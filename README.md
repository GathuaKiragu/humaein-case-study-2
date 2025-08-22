
# Web Automation Agent 

A simple tool that can send emails automatically through Gmail or Outlook.
It takes plain English instructions (like *"send email to [john@example.com](mailto:john@example.com) saying hello"*) and does the job for you.

---

## Requirements

* Python 3.8+
* Google Chrome or Microsoft Edge (Playwright will install what’s needed)
* Test Gmail/Outlook accounts

---

## Setup

1. **Clone the project**

   ```bash
   git clone <repo-url>
   cd humaein-case-study-2
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate   # Mac/Linux
   venv\Scripts\activate      # Windows
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   playwright install
   ```

4. **Set environment variables (credentials)**

   ```bash
   export GMAIL_EMAIL="your-email@gmail.com"
   export GMAIL_PASSWORD="your-app-password"
   export OUTLOOK_EMAIL="your-email@outlook.com"
   export OUTLOOK_PASSWORD="your-password"
   ```

---

## Usage

```bash
# Gmail
python main.py "send email to john@example.com saying hello" --provider gmail

# Outlook
python main.py "send email to jane@example.com saying hi" --provider outlook

# Both
python main.py "send email to test@example.com saying test" --provider both
```

Run with `--headless` to hide the browser.

---

## Notes

* Use Gmail **App Passwords**, not your real password
* Test with demo accounts
* Screenshots are saved if something goes wrong

