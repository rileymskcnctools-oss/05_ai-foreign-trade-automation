# Knowledge Injection Template

## Role
This is a system-level prompt template for injecting domain knowledge into LLM requests.

## Purpose
When generating any content for a product, this knowledge block should be prepended to the main prompt to ensure the LLM has full context about:
- Product specifications
- Target market characteristics
- Keyword strategy
- Competitor landscape

## Template Structure

```
=== PRODUCT KNOWLEDGE ===
Product: {{product_name_en}} ({{product_code}})
Category: {{category}} / {{sub_category}}
Material: {{material}}
Handle: {{handle_material}}
Dimensions: {{length_cm}}cm / {{weight_kg}}kg
MOQ: {{moq}}
Packaging: {{packaging_type}}, {{qty_per_carton}}/ctn
Keywords: {{target_keywords}}
Use Case: {{use_scenario}}
Target Markets: {{target_markets}}
Selling Angle: {{selling_angle}}
Competitor Reference: {{competitor_ref}}

=== MARKET KNOWLEDGE ===
{{market_knowledge_for_country}}

=== KEYWORD DATABASE ===
{{relevant_keywords}}

=== STYLE GUIDE ===
- Tone: Professional B2B
- Language: English
- No prices unless explicitly requested
- Focus on quality, reliability, and value
- Avoid AI-isms (e.g., "game-changer", "revolutionary", "cutting-edge")
- Use specific, measurable claims when possible
```

## Usage
This template is NOT used standalone. It is assembled by the Python code (utils/prompts.py) and prepended to task-specific prompts (SEO, detail page, social media, etc.) before sending to the LLM.
