**Trade Hills Telegram Bot**

A simple Telegram bot for Trade Hills that calculates position sizing based on available funds and risk percentage.

---

## 📋 Features

* `/calculate <funds> <risk_percent>`: Computes the margin amount (funds × risk %) and returns a formatted response.
* Optional group restriction: Bot can be scoped to respond only within a specified Telegram group.
* Fully containerized for deployment on Google Cloud Run.
* CI/CD pipeline via Cloud Build + GitHub trigger for automated builds and deployments.

---

## 🔧 Prerequisites

* **Git** installed locally.
* **Python 3.11+**
* **gcloud CLI** (for GCP deployments) or **Cloud Shell** access.
* A **Telegram Bot Token** (from BotFather).
* A **Telegram Group ID** (for optional scoping).
* A **Google Cloud Project** with billing enabled.

---

## 🚀 Local Development

1. **Clone the repo**

   ```bash
   git clone https://github.com/vicxojsks/tradehills-telegram-bot.git
   cd tradehills-telegram-bot
   ```

2. **Create a virtual environment & install dependencies**

   ```bash
   python3 -m venv venv
   source venv/bin/activate    # macOS/Linux
   venv\\Scripts\\activate   # Windows
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   Create a `.env` file in the project root with:

   ```env
   TOKEN=123456789:ABCDefGhIJkLmNoPQRstuVwxyZ    # Your BotFather token
   GROUP_ID=-1001234567890                      # Your Telegram group ID (optional)
   ```

4. **Run the bot locally**

   ```bash
   python bot.py
   ```

5. In Telegram, send:

   ```
   /calculate 43327.45 5
   ```

   You should see your margin calculation response.

---

## 🐳 Docker

Build and test the container locally:

```bash
docker build -t tradehills-bot .
docker run --env-file .env tradehills-bot
```

---

## ☁️ Deployment on Google Cloud Run

### Manual Deploy

1. **Enable required services**

   ```bash
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com
   ```

2. **Deploy**

   ```bash
   gcloud run deploy tradehills-bot \
     --source . \
     --region us-central1 \
     --platform managed \
     --allow-unauthenticated \
     --set-env-vars TOKEN=$TOKEN,GROUP_ID=$GROUP_ID \
     --runtime python311
   ```

3. Verify in Telegram:

   ```
   /calculate 10000 2.5
   ```

### CI/CD with Cloud Build + GitHub Trigger

1. Add `cloudbuild.yaml` to the repo root (already included).

2. **Enable Cloud Build & Run**

   ```bash
   gcloud services enable cloudbuild.googleapis.com run.googleapis.com
   ```

3. **Grant permissions** to the Cloud Build service account (will be created on first build) or manually create `cloud-build-sa` and assign **Cloud Run Admin** (`roles/run.admin`) and **Service Account User** (`roles/iam.serviceAccountUser`).

4. **Connect GitHub** in the GCP Console under Cloud Build → Triggers → Connect repository (`tradehills-telegram-bot`).

5. **Create a Trigger**:

   * **Event**: Push to the `main` branch
   * **Build config**: `cloudbuild.yaml`
   * **Substitutions**:

     ```text
     _TOKEN    = <YOUR_TELEGRAM_BOT_TOKEN>
     _GROUP_ID = <YOUR_TELEGRAM_GROUP_ID>
     ```

6. **Push** any commit to `main` and watch the pipeline automatically build and deploy to Cloud Run.

---

## ⚙️ Managing Secrets

* Do **not** commit your token or group ID to source control.
* Use **Cloud Build substitutions** or **Cloud Run environment variables** for secure injection.

---

## 🆘 Finding Your IDs

* **Bot Token**: From @BotFather (copy/paste the API token).
* **Group ID**: Use the `getUpdates` API or add @getidsbot to your group and run `/getid`.

---

## 🤝 Contributing

Feel free to submit pull requests or open issues for improvements!

---

Maintained by **Trade Hills** 🧠
