"""
FT Workspace v2.0 - Prompt Template Manager

Load prompt templates from prompts/ directory and fill with product data.

Usage:
    from src.utils.prompts import load_prompt, fill_prompt

    # Load a prompt template
    template = load_prompt("seo/alibaba_title")

    # Fill with product data
    filled = fill_prompt(template, product_dict)
"""

import os
import re
from typing import Optional, Any


def _find_prompts_dir() -> str:
    """Find the prompts/ directory."""
    current = os.path.dirname(os.path.abspath(__file__))
    # Go up from src/utils/ to project root
    for _ in range(3):
        candidate = os.path.join(current, "prompts")
        if os.path.isdir(candidate):
            return candidate
        current = os.path.dirname(current)
    return os.path.join(os.getcwd(), "prompts")


def load_prompt(name: str, prompts_dir: Optional[str] = None) -> str:
    """
    Load a prompt template file.

    Args:
        name: Template name without extension.
              Examples: "seo/alibaba_title", "social/whatsapp", "outreach/rfq_reply"
        prompts_dir: Override prompts directory path.

    Returns:
        Prompt template text.
    """
    if prompts_dir is None:
        prompts_dir = _find_prompts_dir()

    # Try .md extension
    path = os.path.join(prompts_dir, f"{name}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()

    raise FileNotFoundError(
        f"Prompt template not found: {name}.md\n"
        f"Searched in: {prompts_dir}\n"
        f"Available templates: {list_available_templates(prompts_dir)}"
    )


def fill_prompt(template: str, data: dict, strict: bool = False) -> str:
    """
    Fill a prompt template with data.

    Replaces {key} placeholders in the template with values from data dict.

    Args:
        template: Prompt template text with {placeholder} markers.
        data: Dict of placeholder keys to values.
        strict: If True, raise error for missing placeholders.
                If False, leave unfilled placeholders as-is.

    Returns:
        Filled prompt text.
    """
    # Support both {key} and ${key} formats
    # First replace ${key} (v1.0 format)
    def replace_dollar(match):
        key = match.group(1)
        if key in data:
            val = data[key]
            return str(val) if val is not None else ""
        elif strict:
            raise KeyError(f"Missing data for placeholder: ${{{key}}}")
        else:
            return match.group(0)

    result = re.sub(r'\$\{(\w+)\}', replace_dollar, template)

    # Then replace {key} (v2.0 format)
    def replace_brace(match):
        key = match.group(1)
        if key in data:
            val = data[key]
            return str(val) if val is not None else ""
        elif strict:
            raise KeyError(f"Missing data for placeholder: {{{key}}}")
        else:
            return match.group(0)

    return re.sub(r'(?<!\$)\{(\w+)\}', replace_brace, result)


def fill_and_send(
    prompt_name: str,
    data: dict,
    llm_client=None,
    prompts_dir: Optional[str] = None,
    **llm_kwargs
) -> str:
    """
    Load prompt, fill with data, send to LLM, return response.

    Args:
        prompt_name: Template name (e.g., "seo/alibaba_title").
        data: Product data dict.
        llm_client: LLMClient instance. Creates one if None.
        prompts_dir: Override prompts directory.
        **llm_kwargs: Passed to LLMClient.chat().

    Returns:
        LLM response text.
    """
    template = load_prompt(prompt_name, prompts_dir)
    filled = fill_prompt(template, data)

    if llm_client is None:
        from src.core.llm_client import LLMClient
        llm_client = LLMClient()

    return llm_client.chat(filled, **llm_kwargs)


def list_available_templates(prompts_dir: Optional[str] = None) -> list[str]:
    """List all available prompt templates."""
    if prompts_dir is None:
        prompts_dir = _find_prompts_dir()

    templates = []
    for root, dirs, files in os.walk(prompts_dir):
        for f in files:
            if f.endswith(".md"):
                full_path = os.path.join(root, f)
                rel_path = os.path.relpath(full_path, prompts_dir)
                name = os.path.splitext(rel_path)[0]
                templates.append(name)

    return sorted(templates)


def build_product_data(product: dict) -> dict:
    """
    Build a flat data dict from a product record for prompt filling.

    Handles special cases:
    - Converts None to empty string
    - Flattens nested structures
    - Adds combined fields like 'specifications'
    """
    data = {}
    for key, value in product.items():
        if value is not None:
            data[key] = str(value)
        else:
            data[key] = ""

    # Build combined fields if raw data exists
    specs = []
    if product.get("material"):
        specs.append(f"Material: {product['material']}")
    if product.get("handle_material"):
        specs.append(f"Handle: {product['handle_material']}")
    if product.get("length_cm"):
        specs.append(f"Length: {product['length_cm']}cm")
    if product.get("weight_kg"):
        specs.append(f"Weight: {product['weight_kg']}kg")
    if product.get("tine_count"):
        specs.append(f"Tines: {product['tine_count']}")
    if product.get("surface_treatment"):
        specs.append(f"Surface: {product['surface_treatment']}")
    if product.get("hardness"):
        specs.append(f"Hardness: {product['hardness']}")

    data["specifications"] = "\n".join(specs) if specs else "N/A"

    return data
