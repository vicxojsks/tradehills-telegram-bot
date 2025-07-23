# 📈 Trade Hills Telegram Bot for Google Cloud Run

This bot calculates risk-based margin for trading position sizing.

## 🚀 Deployment Instructions

### 1. Requirements
- Google Cloud account
- Enable Cloud Run, Cloud Build
- Install gcloud CLI or use Cloud Shell

### 2. Deploy
```bash
gcloud run deploy tradehills-bot \
  --source . \
  --entry-point bot.py \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars TOKEN=your_token,GROUP_ID=your_group_id \
  --runtime python311
```

### 3. Telegram Usage
```
/calculate 43327.45 5
```

---

Maintained by Trade Hills 🧠
