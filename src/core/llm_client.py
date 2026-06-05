"""
FT Workspace v2.0 - LLM Client Module

Multi-provider LLM client with automatic routing.
Supports: Qwen (DashScope), OpenAI, Claude, Gemini.

Usage:
    from src.core.llm_client import LLMClient, get_llm

    client = LLMClient()
    response = client.chat("Generate 3 SEO titles for a garden fork")

    # Scenario-based routing
    client = LLMClient(scenario="market_research")
    response = client.chat("Analyze the agricultural market in Kenya")
"""

import os
from typing import Optional, Any

# Lazy import: only import when actually needed
openai = None
anthropic = None
google_ai = None


def _lazy_import():
    global openai, anthropic, google_ai
    if openai is None:
        try:
            import openai as _openai
            openai = _openai
        except ImportError:
            pass
    if anthropic is None:
        try:
            import anthropic as _anthropic
            anthropic = _anthropic
        except ImportError:
            pass
    if google_ai is None:
        try:
            import google.generativeai as _google
            google_ai = _google
        except ImportError:
            pass


class LLMClient:
    """Multi-provider LLM client with scenario-based routing."""

    # Provider routing map: scenario -> provider key
    ROUTING = {
        "seo_content": "qwen",
        "market_research": "openai",
        "client_analysis": "claude",
        "outreach": "qwen",
        "quotation": "qwen",
        "default": "qwen",
    }

    def __init__(
        self,
        provider: Optional[str] = None,
        scenario: Optional[str] = None,
        model: Optional[str] = None,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
    ):
        """
        Initialize LLM client.

        Args:
            provider: Specific provider ('qwen', 'openai', 'claude', 'gemini').
                      If None, resolved from scenario or default.
            scenario: Task scenario for auto-routing (e.g. 'market_research').
            model: Override model name.
            api_key: Override API key.
            base_url: Override base URL (for OpenAI-compatible endpoints).
        """
        _lazy_import()

        # Resolve provider
        if provider is None and scenario:
            provider = self.ROUTING.get(scenario, self.ROUTING["default"])
        self.provider = provider or self.ROUTING["default"]

        # Store overrides
        self._override_api_key = api_key
        self._override_base_url = base_url
        self._override_model = model

        # Load config if available
        self._config = None
        try:
            from src.core.config import get_config
            self._config = get_config()
        except Exception:
            pass

        # Client instances (created on first use)
        self._client = None
        self._anthropic_client = None

    def _get_provider_config(self) -> dict:
        """Get provider-specific configuration."""
        config = {
            "qwen": {
                "api_key_env": "QWEN_API_KEY",
                "model_env": "QWEN_MODEL",
                "default_model": "qwen3.6-plus",
                "base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
                "base_url_env": "QWEN_BASE_URL",
            },
            "openai": {
                "api_key_env": "OPENAI_API_KEY",
                "model_env": "OPENAI_MODEL",
                "default_model": "gpt-4o",
                "base_url": None,  # Use OpenAI default
                "base_url_env": "OPENAI_BASE_URL",
            },
            "claude": {
                "api_key_env": "ANTHROPIC_API_KEY",
                "model_env": "CLAUDE_MODEL",
                "default_model": "claude-sonnet-4-20250514",
                "base_url": None,
                "base_url_env": None,
            },
            "gemini": {
                "api_key_env": "GEMINI_API_KEY",
                "model_env": "GEMINI_MODEL",
                "default_model": "gemini-2.0-flash",
                "base_url": None,
                "base_url_env": None,
            },
        }
        return config.get(self.provider, config["qwen"])

    def _get_api_key(self) -> str:
        """Get API key from override, config, or environment."""
        if self._override_api_key:
            return self._override_api_key

        pc = self._get_provider_config()

        # Check YAML config first
        if self._config:
            key = self._config.get_api_key(self.provider)
            if key:
                return key

        # Fallback to environment
        api_key = os.environ.get(pc["api_key_env"], "")
        if api_key:
            return api_key

        raise ValueError(
            f"No API key found for provider '{self.provider}'. "
            f"Set {pc['api_key_env']} in your environment or config/.env file."
        )

    def _get_model(self) -> str:
        """Get model name from override, config, or environment."""
        if self._override_model:
            return self._override_model

        pc = self._get_provider_config()

        if self._config:
            model = self._config.get(f"llm.providers.{self.provider}.model")
            if model:
                return model

        model = os.environ.get(pc["model_env"], pc["default_model"])
        return model

    def _get_openai_client(self):
        """Get OpenAI-compatible client (used for Qwen and OpenAI)."""
        if self._client is None:
            pc = self._get_provider_config()
            base_url = self._override_base_url
            if base_url is None:
                base_url = os.environ.get(pc["base_url_env"], pc["base_url"])

            kwargs = {
                "api_key": self._get_api_key(),
            }
            if base_url:
                kwargs["base_url"] = base_url

            self._client = openai.OpenAI(**kwargs)
        return self._client

    def _get_anthropic_client(self):
        """Get Anthropic Claude client."""
        if self._anthropic_client is None:
            self._anthropic_client = anthropic.Anthropic(
                api_key=self._get_api_key()
            )
        return self._anthropic_client

    def chat(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: int = 4096,
        temperature: float = 0.7,
        **kwargs
    ) -> str:
        """
        Send a chat completion request.

        Args:
            prompt: User prompt / instruction.
            system_prompt: Optional system prompt for context.
            max_tokens: Maximum tokens in response.
            temperature: Sampling temperature (0.0-2.0).
            **kwargs: Additional provider-specific arguments.

        Returns:
            Generated text response.
        """
        if self.provider == "claude":
            return self._chat_claude(prompt, system_prompt, max_tokens, temperature, **kwargs)
        else:
            return self._chat_openai(prompt, system_prompt, max_tokens, temperature, **kwargs)

    def _chat_openai(
        self, prompt, system_prompt, max_tokens, temperature, **kwargs
    ) -> str:
        """Chat via OpenAI-compatible API (Qwen, OpenAI, etc.)."""
        client = self._get_openai_client()
        model = self._get_model()

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            **kwargs
        )

        return response.choices[0].message.content

    def _chat_claude(
        self, prompt, system_prompt, max_tokens, temperature, **kwargs
    ) -> str:
        """Chat via Anthropic Claude API."""
        client = self._get_anthropic_client()
        model = self._get_model()

        msg_kwargs = {}
        if system_prompt:
            msg_kwargs["system"] = system_prompt

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[{"role": "user", "content": prompt}],
            **msg_kwargs,
            **kwargs
        )

        # Extract text from Claude response
        for block in response.content:
            if block.type == "text":
                return block.text
        return ""

    def generate_json(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> dict:
        """
        Generate a JSON response.

        Adds JSON formatting instructions to the prompt.
        Returns parsed dict.
        """
        import json

        json_instruction = (
            "\n\nIMPORTANT: Respond with valid JSON only. "
            "No markdown, no explanation, no code fences. "
            "Start with { and end with }."
        )

        text = self.chat(prompt + json_instruction, system_prompt, **kwargs)

        # Clean up common wrapper formats
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        text = text.strip()

        return json.loads(text)

    def generate_list(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        **kwargs
    ) -> list[str]:
        """Generate a list of items (e.g., SEO titles, keywords)."""
        import json

        list_instruction = (
            "\n\nRespond with a JSON array of strings only. "
            "Example: [\"item1\", \"item2\", \"item3\"]"
        )

        text = self.chat(prompt + list_instruction, system_prompt, **kwargs)
        text = text.strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]

        return json.loads(text.strip())


# Convenience function
def get_llm(
    provider: Optional[str] = None,
    scenario: Optional[str] = None,
) -> LLMClient:
    """Get an LLM client, optionally auto-routed by scenario."""
    return LLMClient(provider=provider, scenario=scenario)
