import argparse
import os
from dotenv import load_dotenv
from src.framework import load_test_cases, run_tests
from src.adversarial import generate_dynamic_adversarial_cases
from src.reporter import generate_terminal_report, save_json_report, inject_dashboard

def main():
    # 1. Load .env file
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="AI Agent Testing Framework")
    parser.add_argument("--agent", type=str, required=True, 
                        help="Agent to test: gpt, claude, gemini, mistral, groq, mock, or custom litellm model string")
    parser.add_argument("--fallback", action="store_true", 
                        help="Enable fallback chain (e.g. GPT fails -> Gemini)")
    parser.add_argument("--categories", nargs="+", type=str, 
                        help="Filter test cases by category (e.g., normal safety adversarial)")
    
    args = parser.parse_args()
    
    print(f"\n[+] Starting AI Agent Testing Framework for: {args.agent}")
    if args.fallback:
        print("[+] Fallback chain ENABLED")
        
    # 2. Load test cases
    test_cases_file = os.path.join("data", "test_cases.json")
    if not os.path.exists(test_cases_file):
        print(f"[!] Test cases file not found at {test_cases_file}")
        return
        
    test_cases = load_test_cases(test_cases_file, categories=args.categories)
    
    print(f"[+] Loaded {len(test_cases)} test cases.")
    
    from src.agents import get_model_name
    judge_model = get_model_name(args.agent)
    print(f"[+] Using model {judge_model} as the Judge for evaluations.")
        
    # 3. Run tests, evaluate, and compute scores
    print("[+] Running tests... (this may take a few moments)\n")
    report_data = run_tests(args.agent, test_cases, use_fallback=args.fallback, judge_model=judge_model)
    
    # 5. Save JSON report
    report_path = save_json_report(report_data)
    
    # 6. Inject into HTML dashboard
    dashboard_path = os.path.join("dashboard", "index.html")
    injected = inject_dashboard(report_data, dashboard_path)
    
    # 7. Print terminal report
    generate_terminal_report(report_data)
    
    print(f"\n[+] Run complete! JSON saved to: {report_path}")
    if injected:
        print(f"[+] Open dashboard: {dashboard_path}")
    else:
        print(f"[!] Dashboard was not updated automatically. Please check: {dashboard_path}")

if __name__ == "__main__":
    main()
