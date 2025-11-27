## Render Deployment Troubleshooting

If you encounter a **502 Bad Gateway** error when deploying to Render:

1. **Check Logs**  
   Go to your Render dashboard and open the **Logs** tab for your service. Review recent error messages, especially Python tracebacks or missing variable warnings.

2. **Verify Environment Variables**  
   In the "Environment" tab, confirm:
   - `OPENAI_API_KEY` is set (case-sensitive)
   - The value is a valid OpenAI API key (begins with `sk-` or `sk-proj-`)

3. **Manual Redeploy**  
   After making changes, trigger a redeploy:
   - Go to "Manual Deploy"
   - Click **Deploy latest commit**
   - Wait for the build to complete

4. **Listen on Render's Assigned Port**  
   Your application must bind to the `$PORT` environment variable supplied by Render:
   ```bash
   uvicorn src.web:app --host 0.0.0.0 --port $PORT
   ```

5. **Still Failing?**  
   Copy and paste the last 20–30 lines of your service logs and seek targeted support.

---

_Add this section to your DEPLOYMENT.md for improved support!_