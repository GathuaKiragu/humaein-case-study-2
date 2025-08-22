# web_agent.py
import json
from typing import Dict, Any
from playwright.sync_api import Page, sync_playwright
import logging

class InstructionParser:
    """Mock LLM that parses natural language into structured commands."""
    
    @staticmethod
    def parse_instruction(instruction: str) -> Dict[str, Any]:
        """
        Parse natural language instruction into structured format.
        In a real system, this would call an actual LLM API.
        """
        instruction = instruction.lower()
        
        # Simple rule-based parsing for the demo
        if "send email" in instruction or "send an email" in instruction:
            return InstructionParser._parse_email_instruction(instruction)
        else:
            # Default to email for this demo
            return InstructionParser._parse_email_instruction(instruction)
    
    @staticmethod
    def _parse_email_instruction(instruction: str) -> Dict[str, Any]:
        """Parse email-specific instructions."""
        # This is a very simple parser - real LLM would be much more sophisticated
        result = {
            "action": "send_email",
            "parameters": {
                "recipient": "",
                "subject": "",
                "body": ""
            }
        }
        
        # Extract recipient
        if "to " in instruction:
            start_idx = instruction.find("to ") + 3
            end_idx = instruction.find(" ", start_idx)
            if end_idx == -1:
                end_idx = len(instruction)
            result["parameters"]["recipient"] = instruction[start_idx:end_idx].strip()
        
        # Extract subject
        if "about " in instruction:
            start_idx = instruction.find("about ") + 6
            end_idx = instruction.find(" with ", start_idx)
            if end_idx == -1:
                end_idx = len(instruction)
            result["parameters"]["subject"] = instruction[start_idx:end_idx].strip()
        
        # Extract body
        if "saying " in instruction or "message " in instruction:
            start_idx = max(instruction.find("saying ") + 7, instruction.find("message ") + 8)
            result["parameters"]["body"] = instruction[start_idx:].strip().strip('"\'')
        
        return result
    
    # web_agent.py (continued)
class GenericWebAgent:
    """Base class for all web automation agents."""
    
    def __init__(self, provider: str, headless: bool = False):
        self.provider = provider
        self.headless = headless
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.logger = logging.getLogger(f"{provider}_agent")
        
    def execute_instruction(self, parsed_instruction: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a parsed instruction. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute_instruction")
    
    def login(self):
        """Login to the service. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement login")
    
    def _take_screenshot(self, name: str):
        """Helper method to take screenshots for debugging."""
        self.page.screenshot(path=f"screenshot_{name}_{datetime.now().timestamp()}.png")
    
    def close(self):
        """Clean up resources."""
        self.context.close()
        self.browser.close()
        self.playwright.stop()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # web_agent.py (continued)
class GenericWebAgent:
    """Base class for all web automation agents."""
    
    def __init__(self, provider: str, headless: bool = False):
        self.provider = provider
        self.headless = headless
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=headless)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()
        self.logger = logging.getLogger(f"{provider}_agent")
        
    def execute_instruction(self, parsed_instruction: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a parsed instruction. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement execute_instruction")
    
    def login(self):
        """Login to the service. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement login")
    
    def _take_screenshot(self, name: str):
        """Helper method to take screenshots for debugging."""
        self.page.screenshot(path=f"screenshot_{name}_{datetime.now().timestamp()}.png")
    
    def close(self):
        """Clean up resources."""
        self.context.close()
        self.browser.close()
        self.playwright.stop()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()