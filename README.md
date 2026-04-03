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

### Running the Project (Beginner Friendly)

This project allows you to evaluate AI agents automatically. The instructions below will show you how to run it in Visual Studio Code (VS Code) or the Command Prompt (CMD).

#### Setup (Required for both methods)
1. **Install Python**: Make sure you have Python installed on your computer. You can download it from [python.org](https://www.python.org/downloads/). During installation, make sure to check the box that says "Add Python to PATH".
2. **Open the project**: Extract the project folder and remember its location.
3. **Environment Setup**:
   - Rename the file `.env.example` to `.env`.
   - Open the `.env` file in a text editor.
   - If you want to use real AI models (like ChatGPT or Gemini), add your API keys to this file. If you just want to test if the project works without API keys, you can skip this step and use the `mock` agent.

#### Option 1: Running in VS Code
1. Open VS Code.
2. Go to `File` > `Open Folder...` and select the project folder.
3. Open a new terminal by clicking `Terminal` > `New Terminal` in the top menu.
4. Install the required libraries by typing the following command and pressing Enter:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the project using the built-in test agent by typing:
   ```bash
   python main.py --agent mock
   ```
6. (Optional) If you added API keys in the `.env` file, you can test real AI models. For example, to test OpenAI's GPT:
   ```bash
   python main.py --agent gpt
   ```

#### Option 2: Running in Command Prompt (CMD)
1. Open the Command Prompt on your computer (Search for `cmd` in the Start menu).
2. Navigate to the project folder using the `cd` command. For example:
   ```cmd
   cd C:\Users\YourName\Documents\AgentTestingFramework
   ```
3. Install the required libraries by typing the following command and pressing Enter:
   ```cmd
   pip install -r requirements.txt
   ```
4. Run the project using the built-in test agent by typing:
   ```cmd
   python main.py --agent mock
   ```
5. (Optional) If you added API keys in the `.env` file, test a real model:
   ```cmd
   python main.py --agent gpt
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
