# 🚨 CRITICAL FIX REQUIRED - Environment Variable

## Issue Found

Your Render deployment has the **wrong environment variable name**!

Current configuration shows:
```
envVars:
  - key: Wikipedia
    value: d24e2b305ed499c9c7eda08d29bc7e0b
```

But your application expects:
```
envVars:
  - key: OPENAI_API_KEY
    value: sk-proj-your-actual-openai-key-here
```

---

## How to Fix (2 minutes)

### Step 1: Go to Render Dashboard
1. Visit: https://dashboard.render.com
2. Click on your service: **"oman-wiki-generator"**

### Step 2: Update Environment Variable
1. Click on the **"Environment"** tab (left sidebar)
2. You should see a variable named **"Wikipedia"**
3. Click **"Delete"** or edit it to change:
   - **Old Key**: Wikipedia
   - **New Key**: OPENAI_API_KEY
   - **Value**: Your actual OpenAI API key (starts with `sk-proj-...`)

### Step 3: Get Your OpenAI API Key
If you don't have it:
1. Go to: https://platform.openai.com/api-keys
2. Create a new key or copy an existing one
3. It should look like: `sk-proj-xxxxxxxxxxxxxxxxxxxxxxxx`

### Step 4: Add the Correct Variable
1. In Render Environment tab, click **"Add Environment Variable"**
2. **Key**: `OPENAI_API_KEY`
3. **Value**: Paste your actual OpenAI API key
4. Click **"Save Changes"**

### Step 5: Wait for Auto-Redeploy
- Render will automatically restart your service (takes ~2-3 minutes)
- Watch the "Events" or "Logs" tab to see progress
- Look for "Deploy successful" or "Live" status

---

## Why This Matters

Your application code looks for the environment variable `OPENAI_API_KEY`:

```python
# In src/wiki_generator.py
api_key = os.getenv("OPENAI_API_KEY")
```

Without the correct variable name, your API will fail when trying to generate articles with errors like:
- "No API key provided"
- "Authentication failed"
- "OpenAI API error"

---

## What's Deployed Now

✅ **Fixed Issues:**
- Dockerfile now properly uses `$PORT` variable from Render
- render.yaml updated with correct Docker configuration
- Auto-deploy is enabled (pushes trigger redeployment)

⚠️ **Still Needs Fixing:**
- Environment variable name must be changed from "Wikipedia" to "OPENAI_API_KEY"
- You need to provide your actual OpenAI API key

---

## Test After Fix

Once you've updated the environment variable and the service shows "Live", test with:

```bash
# Find your Render URL in the dashboard (top of service page)
# It should look like: https://oman-wiki-generator-xxxx.onrender.com

# Test health endpoint
curl https://your-render-url.onrender.com/health

# Expected response:
# {"status":"healthy","service":"oman-wiki-generator"}

# Test article generation
curl -X POST "https://your-render-url.onrender.com/generate/article" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Muscat Festival", "language": "en"}'
```

---

## Your Render URL

Look at the **top of your service page** in Render dashboard. It shows your live URL:
- Format: `https://oman-wiki-generator-[something].onrender.com`
- Or: `https://oman-wiki-generator.onrender.com`

Copy that URL and share it here so I can test your live API!

---

## Summary

**What I've Done:**
1. ✅ Fixed Dockerfile to use PORT variable correctly
2. ✅ Updated render.yaml for proper Docker deployment
3. ✅ Pushed changes to GitHub
4. ✅ Auto-deploy triggered on Render

**What You Need to Do:**
1. ⚠️ Change environment variable name from "Wikipedia" to "OPENAI_API_KEY"
2. ⚠️ Add your actual OpenAI API key value
3. ⚠️ Wait for service to redeploy (~2-3 minutes)
4. ✅ Share your Render URL with me to test

Once you fix the environment variable, your API will be **100% functional and live**! 🚀
