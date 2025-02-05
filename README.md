# 📧 autoemail

This script reads email details from a CSV file, generates previews, asks for confirmation, and sends emails using an SMTP server.

## 🚀 Features
✅ Reads email details from a CSV file.  
✅ Ensures required columns are present (`from`, `to`, `subject`, `body`).  
✅ Supports optional fields (`cc`, `bcc`).  
✅ Formats email body dynamically using placeholders (`Hello {name}!` → `Hello Mark!`).  
✅ Previews each email before sending.  
✅ Sends emails using **SMTP authentication**.  
✅ Uses a **Python configuration file (`params.py`)** for SMTP settings.

---

## 🛠️ Installation

### 1️⃣ **Ensure You Have Python Installed**
This script requires **Python 3.6+**. Check your version:

```sh
python --version
```
or
```sh
python3 --version
```

If you see a version lower than 3.6, update Python before proceeding.

---

### 2️⃣ **Clone the Repository**
```sh
git clone git@github.com:cgiuffr/autoemail.git
cd autoemail
```

---

### 4️⃣ **Copy and Configure `params.py`**
The script requires a configuration file.  
**Copy the default config file**:

```sh
cp params_default.py params.py
```

Then **edit `params.py`** with your input CSV file and SMTP credentials.

---

## 📄 Common SMTP Providers

Here are the SMTP settings for some common providers:

| Provider         | SMTP Server              | Port |
|-----------------|--------------------------|------|
| Gmail           | smtp.gmail.com           | 587  |
| Outlook         | smtp.office365.com       | 587  |
| Yahoo Mail      | smtp.mail.yahoo.com      | 465  |
| Zoho Mail       | smtp.zoho.com            | 587  |
| ProtonMail      | mail.protonmail.com      | 465  |

---

## 📄 CSV File Format

Create a CSV file (e.g., `input.csv`) with the following columns:
```csv
from,to,subject,body,cc,bcc,reply-to,name
admin@example.com,user@example.com,Welcome,Hello {name}! Your account is ready.,manager@example.com,support@example.com,reply@example.com,Mark
noreply@example.com,client@example.com,Reminder,Hi {name}! Your subscription expires soon.,manager@example.com,support@example.com,reply@example.com,James
```

### 🔹 Column Explanation
| Column    | Required? | Description |
|-----------|----------|-------------|
| `from`    | ✅ Yes   | Sender's email address |
| `to`      | ✅ Yes   | Recipient's email address |
| `subject` | ✅ Yes   | Email subject |
| `body`    | ✅ Yes   | Email content (supports placeholders like `{name}`, pulling the value from column `{name}`) |
| `cc`      | ❌ No    | Carbon copy recipient (optional) |
| `bcc`     | ❌ No    | Blind carbon copy recipient (optional) |
| `reply-to`| ❌ No    | Reply-to email address (optional) |

---

## ▶️ Running the Script
Run the script:
```sh
python autoemail.py
```

All emails will be previewed:
```
--- Email Preview ---
From: admin@example.com
To: user@example.com
Subject: Welcome
CC: manager@example.com
BCC: support@example.com
Reply-To: reply@example.com
Body: Hello Mark! Your account is ready.
----------------------

--- Email Preview ---
From: noreply@example.com
To: client@example.com
Subject: Reminder
CC: manager@example.com
BCC: support@example.com
Reply-To: reply@example.com
Body: Hi James! Your subscription expires soon.
----------------------
```

After previewing all emails, a **final confirmation** will be requested:
```
Send all emails? (yes/no):
```
- Type **`yes`** to send all emails.
- Type **`no`** to cancel sending.

---

## 🐝 License

This project is licensed under the **Apache-2.0 license**. Free to use and modify.