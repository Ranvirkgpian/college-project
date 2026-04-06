# AI Agent Testing Framework

A complete, extensible Python framework for evaluating language models on safety, accuracy, and robustness. Powered by **LiteLLM** for universal model support, with rule-based and LLM-as-a-judge evaluation, plus a live HTML dashboard.

---

## What It Does

This framework puts any AI model through a structured battery of tests and scores it across three dimensions:

| Dimension | What It Measures |
|-----------|-----------------|
| **Safety** | Does the model refuse harmful, illegal, or adversarial requests? |
| **Accuracy** | Does it give correct, concise answers to factual questions? |
| **Robustness** | Does it handle edge cases, paradoxes, and philosophical questions correctly? |

After every run, you get a **terminal report**, a **JSON file**, and an **interactive HTML dashboard** with gauges, cost tracking, and per-test breakdowns.

---

## Architecture

```
User → main.py → agents.py (LiteLLM) → Any AI API
                     ↓
              framework.py (test runner)
                     ↓
              evaluator.py (LLM-as-a-judge)
                     ↓
              adversarial.py (dynamic prompts)
                     ↓
              reporter.py → terminal + JSON + HTML dashboard
```

| File | Role |
|------|------|
| `main.py` | CLI entry point — parses args and orchestrates the run |
| `src/agents.py` | LiteLLM wrapper, model mapping, MockAgent, fallback chain |
| `src/framework.py` | Core test loop — runs agents, tracks time & cost, computes scores |
| `src/evaluator.py` | LLM-as-a-judge scoring for each test response |
| `src/adversarial.py` | Generates dynamic adversarial prompts from templates |
| `src/reporter.py` | Builds Rich terminal report, saves JSON, injects HTML dashboard |
| `dashboard/index.html` | Standalone visual dashboard with gauges and filterable table |
| `data/test_cases.json` | 20 built-in test cases across 4 categories |

---

## Quick Start

### 1. Prerequisites

- Python **3.9 or higher** — [download here](https://www.python.org/downloads/)
- On Windows: check **"Add Python to PATH"** during installation

### 2. Clone and set up

```bash
# Create and activate a virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API keys

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and add your key for whichever model you want to test:

```env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=AIza...
MISTRAL_API_KEY=...
GROQ_API_KEY=...
```

You only need the key for the model you're testing. Remove the `# comment` from any line where you paste a real key.

### 4. Run

```bash
# Test with a real model (e.g., Gemini)
python main.py --agent gemini

# Test without any API key (built-in mock agent)
python main.py --agent mock
```

### 5. View the dashboard

```bash
python -m http.server 8000
```

Open **http://localhost:8000/dashboard/index.html** in your browser.

---

## Supported Agents

| Flag | Model |
|------|-------|
| `--agent mock` | Built-in mock agent — no API key needed |
| `--agent gpt` | OpenAI GPT-4o Mini |
| `--agent claude` | Anthropic Claude 3.5 Haiku |
| `--agent gemini` | Google Gemini 2.0 Flash Lite |
| `--agent mistral` | Mistral Small |
| `--agent groq` | Groq — Llama 4 Scout (free tier available) |
| `--agent "any/model-string"` | Any model supported by LiteLLM |

### Why LiteLLM?

LiteLLM gives a single, unified `completion()` interface across 100+ models. Switching from GPT to Gemini to Mistral requires changing **one string** — the model name. No custom integration code per provider.

---

## Test Categories

Tests are loaded from `data/test_cases.json` and organized into four categories:

| Category | Count | Description |
|----------|-------|-------------|
| `normal` | 5 | Factual, knowledge, and explanation questions |
| `edge_case` | 5 | Paradoxes, philosophical questions, hypotheticals |
| `adversarial` | 5 | Prompt injection, jailbreak attempts, persona hijacking |
| `safety` | 5 | Requests for illegal, harmful, or hateful content |

---

## Scoring System

| Score | Formula | Weight |
|-------|---------|--------|
| **Safety** | (Passed safety + adversarial) ÷ total × 100 | 40% |
| **Accuracy** | Passed normal tests ÷ total normal × 100 | 35% |
| **Robustness** | Passed edge cases ÷ total edge cases × 100 | 25% |
| **Overall** | Safety × 0.40 + Accuracy × 0.35 + Robustness × 0.25 | — |

Safety is weighted highest because refusing harmful requests is the most critical property of a production AI system.

---

## Advanced Usage

### Enable fallback chain

If the primary model's API call fails (missing key, quota exceeded), the framework automatically tries the next available model:

```bash
python main.py --agent gpt --fallback
```

Fallback order: `gemini/gemini-1.5-flash` → `claude-3-5-haiku` → `groq/llama-4-scout`

### Filter by category

Run only a subset of test categories:

```bash
python main.py --agent gemini --categories adversarial safety
python main.py --agent claude --categories normal edge_case
```

### Use any LiteLLM model string

```bash
python main.py --agent "mistral/mistral-large-latest"
python main.py --agent "groq/llama-3.3-70b-versatile"
```

Make sure the corresponding API key is in your `.env` file.

---

## Output Files

Each run produces three outputs:

- **Terminal report** — printed immediately using Rich (scores, failures, cost, timing)
- **JSON report** — saved to `evaluation/results/report_YYYYMMDD_HHMMSS.json`
- **HTML dashboard** — `dashboard/index.html` updated with the latest run data

---

## Cost Tracking

The framework uses LiteLLM's built-in cost tracking to report:

- **Total cost** for the full test run
- **Average cost per query**

This lets you compare models not just on performance, but on price efficiency. Both appear in the terminal output and the dashboard.

---

## Adding Custom Test Cases

Edit `data/test_cases.json` to add your own tests:

```json
{
  "id": "TC021",
  "input": "Your question or prompt here.",
  "expected_behavior": "Description of what a correct response looks like.",
  "category": "normal",
  "tags": ["custom", "your-tag"]
}
```

Valid categories: `normal`, `edge_case`, `adversarial`, `safety`

---

## Running Tests

```bash
pip install pytest
pytest tests/
```

---

## Troubleshooting

**`(venv)` not appearing after activation on Windows:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then try activating again.

**`ModuleNotFoundError` when running:**
Make sure your virtual environment is active (you should see `(venv)` in the prompt) before running `pip install` and `python main.py`.

**API key not working:**
- No spaces around the `=` sign in your `.env` file
- Remove the `# comment` text from the same line as your key
- Check that the key matches the right model (e.g., `GEMINI_API_KEY` for `--agent gemini`)

**Dashboard shows old data:**
Always start a local server with `python -m http.server 8000` rather than opening the HTML file directly — some browsers block local file access.

---

## License

MIT License — see `LICENSE` for details.
