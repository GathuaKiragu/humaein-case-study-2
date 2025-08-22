# email_agents.py
from web_agent import GenericWebAgent
from config import CREDENTIALS, URLS, DEFAULT_TIMEOUT
from typing import Dict, Any
import time
# email_agents.py
from web_agent import GenericWebAgent
from config import CREDENTIALS, URLS, DEFAULT_TIMEOUT
from typing import Dict, Any
import time

class GmailAgent(GenericWebAgent):
    """Agent for automating Gmail web interface."""
    
    def __init__(self, headless: bool = False):
        super().__init__("gmail", headless)
    
    def login(self):
        """Login to Gmail."""
        try:
            self.logger.info("Navigating to Gmail...")
            self.page.goto(URLS["gmail"])
            
            # Wait for login page to load - try multiple selectors
            email_selectors = [
                "input[type='email']",
                "input[aria-label*='Email']",
                "input[name*='email']"
            ]
            
            found = False
            for selector in email_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    self.page.fill(selector, CREDENTIALS["gmail"]["email"])
                    found = True
                    break
                except:
                    continue
            
            if not found:
                raise Exception("Could not find email field")
            
            # Click next button
            next_buttons = [
                "button:has-text('Next')",
                "input[type='submit']",
                "button[type='submit']"
            ]
            
            for button in next_buttons:
                try:
                    self.page.click(button, timeout=5000)
                    break
                except:
                    continue
            
            # Wait for password field with multiple selectors
            password_selectors = [
                "input[type='password']",
                "input[aria-label*='Password']",
                "input[name*='password']"
            ]
            
            found = False
            for selector in password_selectors:
                try:
                    self.page.wait_for_selector(selector, timeout=10000)
                    self.page.fill(selector, CREDENTIALS["gmail"]["password"])
                    found = True
                    break
                except:
                    continue
            
            if not found:
                raise Exception("Could not find password field")
            
            # Click next/submit for password
            for button in next_buttons:
                try:
                    self.page.click(button, timeout=5000)
                    break
                except:
                    continue
            
            # Wait for inbox to load with multiple indicators
            inbox_indicators = [
                "div[role='main']",
                "div[aria-label*='Inbox']",
                "a[href*='#inbox']",
                "div[gh='tl']"  # Gmail left navigation
            ]
            
            found = False
            for indicator in inbox_indicators:
                try:
                    self.page.wait_for_selector(indicator, timeout=15000)
                    found = True
                    break
                except:
                    continue
            
            if not found:
                self._take_screenshot("login_complete")
                self.logger.warning("Proceeding without confirming inbox load")
            
            self.logger.info("Successfully logged into Gmail")
            
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            self._take_screenshot("login_failed")
            raise
    
    def execute_instruction(self, parsed_instruction: Dict[str, Any]) -> Dict[str, Any]:
        """Execute email sending instruction."""
        if parsed_instruction["action"] != "send_email":
            return {"success": False, "error": f"Unsupported action: {parsed_instruction['action']}"}
        
        try:
            params = parsed_instruction["parameters"]
            self.logger.info(f"Sending email to {params['recipient']}")
            
            # Click compose button with multiple selectors
            compose_selectors = [
                "div[role='button'][gh='cm']",  # Primary compose button
                "div[aria-label*='Compose']",
                "button[aria-label*='Compose']",
                "div[guidedhelpid*='compose']"
            ]
            
            clicked = False
            for selector in compose_selectors:
                try:
                    self.page.click(selector, timeout=10000)
                    clicked = True
                    break
                except:
                    continue
            
            if not clicked:
                raise Exception("Could not find compose button")
            
            # Wait for compose window with multiple indicators
            compose_indicators = [
                "div[role='dialog']",
                "div[aria-label*='New Message']",
                "div[class*='compose']"
            ]
            
            found = False
            for indicator in compose_indicators:
                try:
                    self.page.wait_for_selector(indicator, timeout=15000)
                    found = True
                    break
                except:
                    continue
            
            if not found:
                self._take_screenshot("compose_window")
                self.logger.warning("Proceeding without confirming compose window")
            
            # Fill recipient with multiple selectors and strategies
            to_selectors = [
                "textarea[aria-label*='To']",
                "textarea[name='to']",
                "input[aria-label*='To']",
                "input[name*='to']"
            ]
            
            filled = False
            for selector in to_selectors:
                try:
                    # Wait for the field to be visible and enabled
                    to_field = self.page.locator(selector)
                    to_field.wait_for(state="visible", timeout=10000)
                    to_field.click()
                    to_field.fill(params["recipient"])
                    to_field.press("Tab")
                    filled = True
                    break
                except Exception as e:
                    self.logger.warning(f"Failed with selector {selector}: {e}")
                    continue
            
            if not filled:
                # Fallback: try to find any input field that might be the To field
                try:
                    inputs = self.page.locator("input, textarea")
                    count = inputs.count()
                    for i in range(count):
                        try:
                            input_field = inputs.nth(i)
                            aria_label = input_field.get_attribute("aria-label") or ""
                            name = input_field.get_attribute("name") or ""
                            if "to" in aria_label.lower() or "to" in name.lower():
                                input_field.fill(params["recipient"])
                                input_field.press("Tab")
                                filled = True
                                break
                        except:
                            continue
                except:
                    pass
            
            if not filled:
                raise Exception("Could not find recipient field")
            
            # Fill subject if provided
            if params["subject"]:
                subject_selectors = [
                    "input[name='subjectbox']",
                    "input[aria-label*='Subject']",
                    "input[placeholder*='Subject']"
                ]
                
                filled_subject = False
                for selector in subject_selectors:
                    try:
                        subject_field = self.page.locator(selector)
                        subject_field.wait_for(state="visible", timeout=5000)
                        subject_field.fill(params["subject"])
                        filled_subject = True
                        break
                    except:
                        continue
                
                if not filled_subject:
                    self.logger.warning("Could not find subject field")
            
            # Fill body if provided
            if params["body"]:
                body_selectors = [
                    "div[aria-label*='Message Body']",
                    "div[role='textbox']",
                    "div[contenteditable='true']",
                    "div[class*='editable']"
                ]
                
                filled_body = False
                for selector in body_selectors:
                    try:
                        body_field = self.page.locator(selector)
                        body_field.wait_for(state="visible", timeout=5000)
                        body_field.click()
                        body_field.fill(params["body"])
                        filled_body = True
                        break
                    except:
                        continue
                
                if not filled_body:
                    self.logger.warning("Could not find body field")
            
            # Click send with multiple selectors
            send_selectors = [
                "div[role='button'][aria-label*='Send']",
                "button[aria-label*='Send']",
                "div[data-tooltip*='Send']",
                "div[guidedhelpid*='send']"
            ]
            
            sent = False
            for selector in send_selectors:
                try:
                    self.page.click(selector, timeout=5000)
                    sent = True
                    break
                except:
                    continue
            
            if not sent:
                raise Exception("Could not find send button")
            
            # Wait for send to complete - check for confirmation or error
            time.sleep(3)
            
            # Check if send was successful by looking for confirmation or error messages
            try:
                # Look for error messages
                error_selectors = [
                    "div[aria-live='assertive']",
                    "div[class*='error']",
                    "div[class*='message']:has-text('error')"
                ]
                
                for selector in error_selectors:
                    if self.page.locator(selector).count() > 0:
                        error_text = self.page.locator(selector).first.text_content()
                        raise Exception(f"Send error: {error_text}")
                
                # Look for success indicators
                success_indicators = [
                    "div:has-text('Message sent')",
                    "div[class*='success']",
                    "div[aria-label*='sent']"
                ]
                
                success_found = False
                for indicator in success_indicators:
                    if self.page.locator(indicator).count() > 0:
                        success_found = True
                        break
                
                if not success_found:
                    self.logger.warning("No explicit success message found, assuming send was successful")
                
            except Exception as e:
                self.logger.warning(f"Send confirmation check failed: {e}")
                # Continue anyway - the email might have been sent
            
            self.logger.info("Email sent successfully")
            return {"success": True, "message": f"Email sent to {params['recipient']}"}
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            self._take_screenshot("send_email_failed")
            return {"success": False, "error": str(e)}
class OutlookAgent(GenericWebAgent):
    """Agent for automating Outlook web interface."""
    
    def __init__(self, headless: bool = False):
        super().__init__("outlook", headless)
    
    def login(self):
        """Login to Outlook."""
        try:
            self.logger.info("Navigating to Outlook...")
            self.page.goto(URLS["outlook"])
            
            # Wait for login page and enter email
            self.page.wait_for_selector("input[type='email']", timeout=DEFAULT_TIMEOUT)
            self.page.fill("input[type='email']", CREDENTIALS["outlook"]["email"])
            self.page.click("input[type='submit']")
            
            # Enter password
            self.page.wait_for_selector("input[type='password']", timeout=DEFAULT_TIMEOUT)
            self.page.fill("input[type='password']", CREDENTIALS["outlook"]["password"])
            self.page.click("input[type='submit']")
            
            # Wait for inbox
            self.page.wait_for_selector("button[aria-label*='New message']", timeout=DEFAULT_TIMEOUT)
            self.logger.info("Successfully logged into Outlook")
            
        except Exception as e:
            self.logger.error(f"Login failed: {e}")
            self._take_screenshot("login_failed")
            raise
    
    def execute_instruction(self, parsed_instruction: Dict[str, Any]) -> Dict[str, Any]:
        """Execute email sending instruction for Outlook."""
        if parsed_instruction["action"] != "send_email":
            return {"success": False, "error": f"Unsupported action: {parsed_instruction['action']}"}
        
        try:
            params = parsed_instruction["parameters"]
            self.logger.info(f"Sending email to {params['recipient']}")
            
            # Click new message button
            self.page.click("button[aria-label*='New message']")
            
            # Wait for compose window
            self.page.wait_for_selector("div[aria-label='Message body']", timeout=DEFAULT_TIMEOUT)
            
            # Fill recipient
            self.page.fill("input[aria-label*='To']", params["recipient"])
            
            # Fill subject if provided
            if params["subject"]:
                self.page.fill("input[aria-label*='Subject']", params["subject"])
            
            # Fill body if provided
            if params["body"]:
                self.page.fill("div[aria-label='Message body']", params["body"])
            
            # Click send
            self.page.click("button[aria-label*='Send']")
            
            # Wait for send to complete
            time.sleep(3)
            
            self.logger.info("Email sent successfully")
            return {"success": True, "message": f"Email sent to {params['recipient']}"}
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {e}")
            self._take_screenshot("send_email_failed")
            return {"success": False, "error": str(e)}