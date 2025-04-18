# 🎁 Xbox Gift Card Checker (Undetected Chrome)

<img src="https://i.imgur.com/bn7ojzC.png">

This Python tool uses an **undetected Chromium browser** to log into Microsoft/Xbox accounts and check whether a gift card code is **valid and redeemable** — without actually redeeming it. Valid codes are logged and saved for future use.

Currently, this version is tailored for **Turkish Lira (₺)**. However, it can be easily modified to support other currencies.

---

### ⚙️ Features

- Uses Chromium in undetected mode to bypass bot detection
- Automatically logs into Microsoft accounts using email:password combos
- Checks Xbox/Microsoft gift card codes without redeeming them
- Saves valid codes into a `.txt` file based on their balance
- Handles multi-account, multi-code scenarios with progress tracking
- Designed to mimic human behavior with randomized delays

---

### 📦 Installation

Make sure you have Python 3.8 or later installed.

### 1. Install Dependencies

```bash
pip install DrissionPage loguru
```

Note: You must have Google Chrome installed. The default path is set to /usr/bin/google-chrome, adjust if needed.

---

### 📁 File Structure

- accounts.txt: List of Microsoft accounts in email:password format
- codes.txt: List of gift card codes (one per line)
- progress.txt: Tracks the current index of account and code to resume from where it left off

---

### 🚀 How to Use

- Add your Microsoft account credentials to accounts.txt
- Add the gift card codes you want to check into codes.txt
 
Run the script:
```
python main.py
```

The script will:
- Log into accounts one by one
- Check up to 20 codes per account
- Save valid codes into a file like 100TL.txt
- Resume from where it left off if interrupted

---

### 💡 Notes

- This tool does not redeem the gift card codes — it only checks their validity
- Only works for Turkish currency codes in the current version
- Time delays are added to reduce detection risk
- If Microsoft challenges login (2FA, captchas, etc.), those accounts will fail
- It is proxyless and automatically switches to a new account every 25 codes to avoid rate limiting

---

### ⚠️ Disclaimer
This project is for educational purposes only. Use responsibly and at your own risk. The developer is not responsible for any consequences resulting from the use of this tool.
