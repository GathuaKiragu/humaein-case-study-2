# main.py
#!/usr/bin/env python3
import argparse
import logging
from web_agent import InstructionParser
from email_agents import GmailAgent, OutlookAgent

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="Web Automation Agent")
    parser.add_argument("instruction", help="Natural language instruction (e.g., 'send email to test@example.com saying hello')")
    parser.add_argument("--provider", choices=["gmail", "outlook", "both"], default="gmail", help="Email provider to use")
    parser.add_argument("--headless", action="store_true", help="Run browser in headless mode")
    
    args = parser.parse_args()
    
    # Parse the instruction
    logger.info(f"Parsing instruction: {args.instruction}")
    parsed_instruction = InstructionParser.parse_instruction(args.instruction)
    logger.info(f"Parsed instruction: {parsed_instruction}")
    
    results = {}
    
    try:
        if args.provider in ["gmail", "both"]:
            logger.info("Executing with Gmail...")
            with GmailAgent(headless=args.headless) as agent:
                agent.login()
                results["gmail"] = agent.execute_instruction(parsed_instruction)
        
        if args.provider in ["outlook", "both"]:
            logger.info("Executing with Outlook...")
            with OutlookAgent(headless=args.headless) as agent:
                agent.login()
                results["outlook"] = agent.execute_instruction(parsed_instruction)
        
        # Print results
        print("\n=== EXECUTION RESULTS ===")
        for provider, result in results.items():
            status = "✅ SUCCESS" if result.get("success") else "❌ FAILED"
            print(f"{provider.upper()}: {status}")
            if result.get("success"):
                print(f"  Message: {result.get('message')}")
            else:
                print(f"  Error: {result.get('error')}")
                
    except Exception as e:
        logger.error(f"Execution failed: {e}")
        print(f"❌ Overall execution failed: {e}")

if __name__ == "__main__":
    main()