# 🚀 Quick Deploy Guide - Go Live in 5 Minutes

## Option 1: Render.com (Recommended - FREE)

**Fastest path to production with free tier!**

### Step 1: Push Latest Code
```bash
git add .
git commit -m "chore: add Render deployment config"
git push origin moodi112-patch-1
```

### Step 2: Deploy to Render
1. Go to **[render.com](https://render.com)** and sign up (free)
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub account
4. Select repository: `https-github.com-moodi112-moodi112`
5. Configure:
   - **Name**: `oman-wiki-generator`
   - **Branch**: `moodi112-patch-1`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn src.web:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variable:
   - Key: `OPENAI_API_KEY`
   - Value: `your_openai_api_key_here`
7. Click **"Create Web Service"**

**Your app will be live at**: `https://oman-wiki-generator.onrender.com`

---

## Option 2: Railway.app (Also FREE)

### Quick Deploy
1. Go to **[railway.app](https://railway.app)**
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your repository
5. Add environment variables:
   - `OPENAI_API_KEY=your_key`
   - `PORT=8000`
6. Railway auto-detects Python and deploys!

**Live in 2 minutes!**

---

## Option 3: Heroku (Classic Choice)

### Prerequisites
```bash
# Install Heroku CLI
winget install Heroku.HerokuCLI
```

### Deploy Steps
```bash
# Login to Heroku
heroku login

# Create app
heroku create oman-wiki-generator

# Set environment variables
heroku config:set OPENAI_API_KEY=your_key_here
heroku config:set OPENAI_MODEL=gpt-4

# Deploy
git push heroku moodi112-patch-1:main

# Open your live app
heroku open
```

---

## Option 4: Vercel (Serverless)

1. Install Vercel CLI:
```bash
npm install -g vercel
```

2. Deploy:
```bash
vercel --prod
```

3. Add environment variables in Vercel dashboard:
   - `OPENAI_API_KEY`

---

## Option 5: Local Network (Test Live)

**Make it accessible on your local network right now:**

```bash
# Get your local IP
ipconfig | findstr IPv4

# Start server (accessible to all devices on your network)
uvicorn src.web:app --host 0.0.0.0 --port 8000

# Access from any device on your network:
# http://YOUR_IP_ADDRESS:8000
```

---

## Option 6: Docker + Cloud Run (Google Cloud)

```bash
# Build and push to Google Cloud
gcloud builds submit --tag gcr.io/PROJECT_ID/oman-wiki-generator

# Deploy
gcloud run deploy oman-wiki-generator \
  --image gcr.io/PROJECT_ID/oman-wiki-generator \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=your_key
```

---

## 🎯 Recommended: Render.com

**Why Render?**
- ✅ **FREE tier** (doesn't sleep like Heroku free)
- ✅ Auto-deploys from GitHub
- ✅ Free SSL certificate
- ✅ Custom domains
- ✅ Easy environment variables
- ✅ Build logs and monitoring
- ✅ No credit card required for free tier

---

## After Deployment

### Test Your Live API

```bash
# Replace with your actual URL
curl https://oman-wiki-generator.onrender.com/health

# Generate an article
curl -X POST "https://oman-wiki-generator.onrender.com/generate/article" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Muscat Festival", "language": "en"}'
```

### Share Your Live API

Your documentation will be automatically available at:
- **Homepage**: `https://your-app.onrender.com/`
- **API Docs**: `https://your-app.onrender.com/docs`
- **ReDoc**: `https://your-app.onrender.com/redoc`

---

## Environment Variables Needed

For all platforms, you'll need:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
OPENAI_MODEL=gpt-4
```

Optional:
```env
PORT=8000  # Auto-set by most platforms
```

---

## Custom Domain (Optional)

### Render.com
1. Go to Settings → Custom Domain
2. Add your domain: `wiki.yourdomain.com`
3. Update DNS records as shown

### Cloudflare (Free SSL + CDN)
1. Point domain to your Render/Railway/Heroku URL
2. Enable proxy (orange cloud)
3. Force HTTPS

---

## Monitoring & Maintenance

### Check if Live
```bash
curl https://your-app-url.com/health
```

### View Logs (Render)
- Dashboard → Your Service → Logs tab

### Update Deployment
```bash
git push origin moodi112-patch-1
# Render auto-deploys on push!
```

---

## Cost Estimate

| Platform | Free Tier | Paid Tier |
|----------|-----------|-----------|
| **Render** | ✅ 750 hrs/month | $7/month |
| **Railway** | ✅ $5 credit/month | $0.000231/GB-hour |
| **Heroku** | ❌ Removed free tier | $5/month |
| **Vercel** | ✅ Generous | $20/month |
| **Google Cloud Run** | ✅ 2M requests/month | Pay per use |

---


## 🎉 Go Live NOW!

**Fastest option**: Open [render.com](https://render.com) → Sign up → Deploy in 3 clicks!

Your Oman Wikipe# Test article generation
curl -X POST "https://your-app.onrender.com/generate/article" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Renaissance Day", "language": "en"}'dia Generator will be **LIVE and PUBLIC** within 5 minutes! 🚀
