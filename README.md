# AI Agent Testing Framework

This project is a complete AI Agent Testing Framework built in Python, using LiteLLM as a universal AI connector. It evaluates language models on standard, edge case, safety, and adversarial test cases. It performs rule-based and LLM-as-a-judge evaluations to generate Safety, Accuracy, and Robustness scores, providing detailed terminal and HTML reports.

## Why LiteLLM?

LiteLLM provides a standardized interface for interacting with over 100+ AI models. Instead of writing custom API integration code for OpenAI, Anthropic, Gemini, Mistral, Groq, and others, you write one standard `completion()` call. Adding a new AI model requires changing only ONE string—the model name—making the framework highly extensible and easy to maintain.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Set up environment variables:
   ```bash
   cp .env.example .env
   ```
3. Open `.env` and fill in the API keys for the models you want to use. You only need keys for the specific models you plan to test.

## Quickstart

### Run with zero API keys using the built-in mock agent
```bash
python main.py --agent mock
```

### Run with a real AI model
For example, to test Gemini:
```bash
python main.py --agent gemini
```

### Enable fallback chain
If an API fails or the key is missing, you can test a fallback chain (e.g. GPT -> Gemini -> Claude):
```bash
python main.py --agent gpt --fallback
```

### Filter tests by category
```bash
python main.py --agent gpt --categories adversarial safety
```

## Adding a New AI Model

To test a completely new AI model that isn't built into the shortcuts, just pass its LiteLLM model string to the `--agent` flag. Ensure you have the corresponding API key in your `.env` file!

```bash
python main.py --agent "mistral/mistral-large-latest"
```

## Scoring System

| Score | Description |
|-------|-------------|
| **Safety Score** | (Passed safety + adversarial tests / total) × 100 |
| **Accuracy Score** | (Correct normal responses / total normal tests) × 100 |
| **Robustness Score** | (Passed edge cases / total edge cases) × 100 |
| **Overall Score** | Safety × 0.40 + Accuracy × 0.35 + Robustness × 0.25 |

Safety is heavily weighted because adhering to safety guidelines and resisting jailbreaks is critical for production AI systems.

## Cost Tracking

The framework leverages LiteLLM's built-in cost tracking feature (`response._hidden_params.get("response_cost")`) to calculate the cost per query and the total run cost. This allows you to evaluate models not just on performance, but also on price efficiency. Results are displayed in the terminal and HTML dashboard.
