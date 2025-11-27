# Webhook Setup Guide

This guide explains how to set up Slack and Microsoft Teams webhooks for CI/CD notifications.

## Slack Webhook Setup

### Step 1: Create Incoming Webhook
1. Go to your Slack workspace
2. Navigate to **Apps** → **Browse Apps** → Search for "Incoming Webhooks"
3. Click **Add to Slack**
4. Select the channel where you want notifications (e.g., `#ci-builds`)
5. Click **Add Incoming WebHooks integration**

### Step 2: Copy Webhook URL
1. Slack will generate a webhook URL like: `https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXX`
2. Copy this URL (you'll need it for GitHub Secrets)
3. Optionally customize:
   - **Descriptive Label**: "GitHub Actions CI"
   - **Customize Name**: "CI Pipeline Bot"
   - **Customize Icon**: Upload a CI/CD icon

### Step 3: Add to GitHub Secrets
1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `SLACK_WEBHOOK_URL`
5. Value: Paste the webhook URL from Step 2
6. Click **Add secret**

### Test Your Slack Integration
Run your workflow and check the designated Slack channel for notifications!

---

## Microsoft Teams Webhook Setup

### Step 1: Create Incoming Webhook in Teams
1. Open Microsoft Teams
2. Navigate to the channel where you want notifications
3. Click the **•••** (more options) next to the channel name
4. Select **Connectors** (or **Workflows** in newer Teams versions)

#### For Classic Teams:
5. Search for "Incoming Webhook"
6. Click **Configure**
7. Provide a name: "GitHub Actions CI"
8. Optionally upload an icon
9. Click **Create**
10. Copy the webhook URL (looks like: `https://outlook.office.com/webhook/...`)

#### For New Teams (Workflows):
5. Click **Post to a channel when a webhook request is received**
6. Configure the workflow
7. Copy the generated webhook URL

### Step 2: Add to GitHub Secrets
1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `TEAMS_WEBHOOK_URL`
5. Value: Paste the webhook URL from Step 1
6. Click **Add secret**

### Test Your Teams Integration
Run your workflow and check the Teams channel for notifications!

---

## Codecov Token Setup

### Step 1: Sign Up for Codecov
1. Go to [codecov.io](https://codecov.io)
2. Sign in with your GitHub account
3. Authorize Codecov to access your repositories

### Step 2: Get Repository Token
1. Select your repository from the Codecov dashboard
2. Go to **Settings** → **General**
3. Copy the **Repository Upload Token**

### Step 3: Add to GitHub Secrets
1. Go to your GitHub repository
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `CODECOV_TOKEN`
5. Value: Paste the token from Step 2
6. Click **Add secret**

---

## Verify All Secrets

After adding all three secrets, verify in your repository:

**Settings** → **Secrets and variables** → **Actions**

You should see:
- ✅ `SLACK_WEBHOOK_URL`
- ✅ `TEAMS_WEBHOOK_URL`
- ✅ `CODECOV_TOKEN`

---

## Testing Notifications

### Test with a Simple Commit
```bash
# Make a small change
echo "# Test" >> README.md

# Commit and push
git add README.md
git commit -m "test: trigger CI notifications"
git push
```

### Expected Results
1. **GitHub Actions** runs the workflow
2. **Slack** receives notifications for each job (lint, test, coverage)
3. **Teams** receives notifications for each job
4. **Codecov** receives coverage report

### Troubleshooting

**No notifications received?**
- Verify webhook URLs are correct in GitHub Secrets
- Check that webhooks haven't expired (Teams webhooks can expire)
- Ensure the Slack channel or Teams channel still exists
- Review GitHub Actions logs for error messages

**Codecov upload fails?**
- Verify token is correct
- Check that coverage.xml file was generated
- Ensure Codecov has access to your repository

---

## Notification Customization

### Modify Notification Messages
Edit the workflow file (`.github/workflows/ci.yml`) to customize notification content:

**For Slack:**
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    fields: repo,commit,author,workflow,job
    text: 'Custom message here'  # Add custom text
```

**For Teams:**
```yaml
- name: Notify Teams
  uses: Ilshidur/action-msteams@v2
  with:
    webhook-uri: ${{ secrets.TEAMS_WEBHOOK_URL }}
    title: "Custom Title • ${{ job.status }}"
    summary: "Custom summary message"
```

---

## Security Notes

⚠️ **Never commit webhook URLs or tokens to your repository**  
✅ Always use GitHub Secrets for sensitive information  
✅ Rotate tokens/webhooks if accidentally exposed  
✅ Use separate webhooks for different environments (dev/staging/prod)  

---

## Additional Resources

- [Slack Incoming Webhooks Documentation](https://api.slack.com/messaging/webhooks)
- [Microsoft Teams Webhooks Documentation](https://learn.microsoft.com/en-us/microsoftteams/platform/webhooks-and-connectors/how-to/add-incoming-webhook)
- [Codecov Documentation](https://docs.codecov.com/docs)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
