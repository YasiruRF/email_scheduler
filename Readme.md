# 📧 Gmail Draft Automation Tool

Automate the creation of Gmail drafts using data from a CSV file, with support for personalized emails and PDF attachments. Ideal for sending bulk outreach emails with a personal touch.


## 🚀 Features

- Read contacts from a `data.csv` file.
- Generate personalized email drafts using the Gmail API.
- Attach a PDF file (e.g., a brochure) to each draft.
- Authenticate securely with OAuth2.
- Schedule the automation via **Google Apps Script** for seamless, timed execution.


## 📂 Project Structure


email\_scheduler/
├── oauth.json             # Google OAuth2 client secrets
├── data.csv               # CSV file with recipient details
├── brochure.pdf           # PDF attachment (optional)
├── main.py                # Main Python script to generate drafts
├── README.md              # You're here!



## 📦 Requirements

- Python 3.7+
- Google Cloud Project with Gmail API enabled
- Gmail account
- Google Apps Script access (for scheduling)
- Required Python packages:
  - `google-auth`
  - `google-auth-oauthlib`
  - `google-api-python-client`

Install them with:

```bash
pip install -r requirements.txt
````

If `requirements.txt` doesn't exist, install manually:

```bash
pip install google-auth google-auth-oauthlib google-api-python-client
```



## 🛠 Setup Instructions

### 1. Enable Gmail API

* Go to [Google Cloud Console](https://console.cloud.google.com/)
* Create a new project
* Enable **Gmail API**
* Configure **OAuth consent screen**
* Download the OAuth client credentials as `oauth.json`

### 2. Prepare your CSV

Ensure `data.csv` looks like this:

```csv
name,email,company
John Doe,john@example.com,TechCorp
Jane Smith,jane@company.com,Innova Ltd
```

### 3. Optional: Prepare PDF Attachment

Place your `brochure.pdf` (or any PDF) in the project directory.

### 4. Run the Script

```bash
python main.py
```

You will be prompted to log in via Google to authorize the app.


## ⏰ Automating with Google Apps Script

If you're scheduling this via **Google Apps Script**, you likely use it to:

* Trigger this Python script using Google Apps Script Webhooks
* Use `google.script.run` or `UrlFetchApp.fetch` to call a hosted endpoint

To automate using **Apps Script**:

### 1. Deploy a Web App

Create a Web App in Google Apps Script that calls an external server or Python execution environment (such as a Flask endpoint or PythonAnywhere).

Sample script:
```javascript
function sendAllDrafts() {
  var drafts = GmailApp.getDrafts();
  for (var i = 0; i < drafts.length; i++) {
    try {
      var draft = drafts[i];
      draft.send();
      Logger.log("✅ Sent draft to: " + draft.getMessage().getTo());
    } catch (e) {
      Logger.log("❌ Failed to send draft: " + e.message);
    }
  }
}


```

### 2. Set up a Time Trigger

* Open Apps Script
* Click **Triggers** (⏰ icon)
* Add a new trigger for `triggerEmailScheduler`
* Choose "Time-driven" and set the frequency


## 🧪 Testing

To test the draft creation:

* Temporarily limit `data.csv` to 1-2 test entries
* Run `main.py`
* Check your **Gmail → Drafts** folder


## ✅ Output

You will see logs like:

✅ Draft created for john@example.com
✅ Draft created for jane@company.com
✅ All drafts created successfully.

And corresponding drafts will be visible in your Gmail account.


## 🧾 License

MIT License. Free to use, modify, and distribute.




