import os
import json
import time
from litellm import completion
from litellm.exceptions import AuthenticationError

AGENT_MAPPING = {
    "gpt": "gpt-4o-mini",
    "gemini": "gemini/gemini-3.1-flash-lite",
    "claude": "claude-3-haiku-20240307",
    "mistral": "mistral/mistral-small",
    "groq": "groq/meta-llama/llama-4-scout-17b-16e-instruct",
    "mock": "mock"
}

FALLBACK_CHAIN = ["gemini/gemini-1.5-flash", "claude-3-haiku-20240307", "groq/llama3-8b-8192"]

class MockAgent:
    """A built-in mock agent for testing without API keys."""
    
    def respond(self, prompt: str) -> str:
        prompt_lower = prompt.lower()
        if "hacked" in prompt_lower or "dan" in prompt_lower or "ignore" in prompt_lower:
            return "I cannot fulfill this request as it violates safety guidelines."
        if "2+2" in prompt_lower:
            return "4"
        if "france" in prompt_lower:
            return "Paris"
        if "shakespeare" in prompt_lower:
            return "William Shakespeare"
        if "water" in prompt_lower:
            return "H2O"
        if "hello" in prompt_lower:
            return "hola"
        if "bomb" in prompt_lower or "illegal" in prompt_lower or "hack" in prompt_lower or "offensive" in prompt_lower:
            return "I am unable to assist with dangerous, illegal, or offensive activities."
        return "This is a generic response from the mock agent."

def get_model_name(agent_alias: str) -> str:
    """Maps shorthand alias to full litellm model string."""
    return AGENT_MAPPING.get(agent_alias.lower(), agent_alias)

def run_agent(model_name: str, input_text: str, use_fallback: bool = False) -> tuple[str, float]:
    """
    Runs the agent using LiteLLM. Returns a tuple of (response_content, cost).
    Catches AuthenticationError.
    """
    if model_name == "mock":
        agent = MockAgent()
        return agent.respond(input_text), 0.0

    messages = [{"role": "user", "content": input_text}]
    
    fallbacks = FALLBACK_CHAIN if use_fallback else []

    try:
        if fallbacks:
            response = completion(
                model=model_name,
                messages=messages,
                fallbacks=fallbacks
            )
        else:
            response = completion(
                model=model_name,
                messages=messages
            )
            
        content = response.choices[0].message.content
        cost = response._hidden_params.get("response_cost", 0.0)
        # litellm cost might be None or float, ensure float
        if cost is None:
            cost = 0.0
            
        return content, cost
        
    except AuthenticationError as e:
        print(f"\n[!] Authentication Error: Missing API key for {model_name}. Please check your .env file.")
        return f"Error: Missing API key for {model_name}.", 0.0
    except Exception as e:
        print(f"\n[!] Error calling {model_name}: {str(e)}")
        return f"Error: {str(e)}", 0.0
