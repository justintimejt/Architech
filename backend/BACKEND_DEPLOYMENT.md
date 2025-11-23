# FastAPI Backend Deployment Guide

This guide covers deploying the BuildFlow FastAPI backend to various platforms.

## Prerequisites

- Python 3.9+ installed locally
- All environment variables configured
- Backend code tested locally

## Required Environment Variables

Set these in your deployment platform:

- `PORT` - Server port (default: 4000, platforms usually set this automatically)
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_SERVICE_ROLE_KEY` - Supabase service role key (keep secret!)
- `GOOGLE_GEMINI_API_KEY` - Google Gemini API key (keep secret!)

---

## Option 1: Render (Recommended - Easiest)

Render is the easiest platform for deploying FastAPI with automatic venv handling.

### Steps:

1. **Create a Render account** at https://render.com

2. **Create a new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select the repository

3. **Configure the service:**
   - **Name:** `buildflow-backend` (or your preferred name)
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Root Directory:** `backend`

4. **Set Environment Variables:**
   - Go to **Environment** tab
   - Add:
     - `SUPABASE_URL` = your Supabase URL
     - `SUPABASE_SERVICE_ROLE_KEY` = your service role key
     - `GOOGLE_GEMINI_API_KEY` = your Gemini API key
   - `PORT` is automatically set by Render (don't set it manually)

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically:
     - Create a virtual environment
     - Install dependencies from `requirements.txt`
     - Start your FastAPI app

6. **Get your backend URL:**
   - After deployment, your backend will be at: `https://your-service-name.onrender.com`
   - Use this URL as `VITE_BACKEND_URL` in your frontend deployment

### Render Notes:
- Free tier includes 750 hours/month (enough for always-on)
- Free tier services spin down after 15 minutes of inactivity (first request after spin-down takes ~30 seconds)
- Upgrade to paid plan for always-on service

---

## Option 2: Fly.io

Fly.io offers great performance and global distribution.

### Steps:

1. **Install Fly CLI:**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login to Fly.io:**
   ```bash
   fly auth login
   ```

3. **Initialize Fly.io in backend directory:**
   ```bash
   cd backend
   fly launch
   ```
   - Follow prompts to create app
   - Don't deploy yet (we need to configure first)

4. **Configure `fly.toml`** (created automatically):
   ```toml
   app = "your-app-name"
   primary_region = "iad"  # Choose closest region

   [build]
     # Fly.io will auto-detect Python

   [http_service]
     internal_port = 4000
     force_https = true
     auto_stop_machines = true
     auto_start_machines = true
     min_machines_running = 0
     processes = ["app"]

   [[services]]
     http_checks = []
     internal_port = 4000
     processes = ["app"]
     protocol = "tcp"
     script_checks = []

     [services.concurrency]
       type = "connections"
       hard_limit = 25
       soft_limit = 20

     [[services.ports]]
       handlers = ["http"]
       port = 80

     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

5. **Set secrets (environment variables):**
   ```bash
   fly secrets set SUPABASE_URL=your_supabase_url
   fly secrets set SUPABASE_SERVICE_ROLE_KEY=your_service_role_key
   fly secrets set GOOGLE_GEMINI_API_KEY=your_gemini_key
   ```

6. **Deploy:**
   ```bash
   fly deploy
   ```

7. **Get your backend URL:**
   - Your backend will be at: `https://your-app-name.fly.dev`
   - Use this as `VITE_BACKEND_URL` in frontend

### Fly.io Notes:
- Free tier includes 3 shared-cpu VMs
- Great for global distribution
- Fast cold starts

---

## Option 3: Railway

Railway offers simple deployment with automatic environment detection.

### Steps:

1. **Create Railway account** at https://railway.app

2. **Create new project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your repository

3. **Configure service:**
   - Railway auto-detects Python
   - Set **Root Directory** to `backend`
   - Railway will automatically:
     - Detect `requirements.txt`
     - Create venv and install dependencies
     - Run the start command

4. **Set environment variables:**
   - Go to **Variables** tab
   - Add:
     - `SUPABASE_URL`
     - `SUPABASE_SERVICE_ROLE_KEY`
     - `GOOGLE_GEMINI_API_KEY`
   - `PORT` is set automatically

5. **Configure start command:**
   - In **Settings** → **Deploy**, set:
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

6. **Deploy:**
   - Railway auto-deploys on git push
   - Or click "Deploy" manually

7. **Get your backend URL:**
   - Railway provides a URL like: `https://your-app.up.railway.app`
   - Use this as `VITE_BACKEND_URL`

### Railway Notes:
- Free tier includes $5 credit/month
- Simple setup, great developer experience
- Auto-deploys on git push

---

## Option 4: DigitalOcean App Platform

### Steps:

1. **Create App Platform app** at https://cloud.digitalocean.com/apps

2. **Connect GitHub repository**

3. **Configure:**
   - **Type:** Web Service
   - **Source:** `backend/` directory
   - **Build Command:** `pip install -r requirements.txt`
   - **Run Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

4. **Set environment variables** in App Settings

5. **Deploy**

---

## Local Testing Before Deployment

Test your deployment configuration locally:

```bash
cd backend

# Activate venv (if not already active)
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export SUPABASE_URL=your_url
export SUPABASE_SERVICE_ROLE_KEY=your_key
export GOOGLE_GEMINI_API_KEY=your_key
export PORT=4000

# Run the app
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Test the health endpoint:
```bash
curl http://localhost:4000/api/health
```

Should return: `{"ok": true}`

---

## Important Notes

### CORS Configuration
The backend is already configured to allow all origins (`allow_origins=["*"]`). For production, you may want to restrict this to your frontend domain:

```python
# In backend/app/main.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",
        "http://localhost:5173",  # For local dev
    ],
    # ... rest of config
)
```

### Port Configuration
- Most platforms set `PORT` automatically via environment variable
- The code reads `PORT` from env (defaults to 4000)
- Use `--port $PORT` in start command to use the platform's port

### Virtual Environment
- **You don't need to commit `venv/`** - platforms create their own
- Add `venv/` to `.gitignore` if not already there
- Platforms automatically create venv from `requirements.txt`

### Health Check
The backend includes a health check endpoint at `/api/health` that platforms can use to verify the service is running.

---

## Troubleshooting

### Import Errors
If you get import errors, ensure:
- `requirements.txt` includes all dependencies
- Root directory is set to `backend/` in platform settings
- Start command uses `app.main:app` (not `main:app`)

### Environment Variables Not Loading
- Verify variables are set in platform dashboard
- Check variable names match exactly (case-sensitive)
- Restart service after adding variables

### Port Already in Use
- Don't hardcode port numbers
- Always use `$PORT` environment variable
- Platform sets this automatically

### CORS Errors
- Verify CORS middleware is configured correctly
- Check frontend is using correct backend URL
- Ensure backend allows your frontend origin

---

## Recommended: Render

For this project, **Render is recommended** because:
- ✅ Easiest setup (no config files needed)
- ✅ Automatic venv handling
- ✅ Free tier available
- ✅ Good documentation
- ✅ Automatic HTTPS
- ✅ Environment variable management

---

## Next Steps

After deploying backend:

1. **Get your backend URL** (e.g., `https://buildflow-backend.onrender.com`)

2. **Update frontend environment variable:**
   - In Vercel (or your frontend platform)
   - Set `VITE_BACKEND_URL=https://your-backend-url.com`
   - **Don't include `/api`** - frontend adds it automatically

3. **Test the connection:**
   - Deploy frontend
   - Try using the AI chat feature
   - Check browser console for any errors

4. **Monitor logs:**
   - Check backend logs in your platform dashboard
   - Look for any errors or warnings

