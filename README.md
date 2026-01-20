# Rōblox Compliance Automator

Do you have many games that risk becoming unplayable and stuff by 2025-09-30?  This program completes the compliance questionnaire for any given experience you have edit access to.

You will need:
1. Python, 
2. Python's `requests` library, and
3. A valid ROBLOSECURITY cookie set as an environment variable named `ROBLOSECURITY`

If you're on Powershell, you can replace `...` with your cookie value and do:
```ps1
pip3 install requests
$env:ROBLOSECURITY = "..."
python3 main.py
```
