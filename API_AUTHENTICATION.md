# API Authentication Guide

## Current Setup

### OpenAI API Key
The application uses the OpenAI API key stored in the `.env` file. This key is:
- **Loaded automatically** from environment variables when the application starts
- **Used internally** by the WikiGenerator class
- **Not exposed** in API requests or responses

### REST API Access
Currently, the FastAPI web service **does not require authentication**. Any client can:
- Make requests to endpoints like `/generate/article`
- Access the interactive documentation at `/docs`
- Use all generation features without credentials

## Security Considerations

### Current State: Open Access
```python
# src/web.py - Current implementation
@app.post("/generate/article")
async def generate_article(request: ArticleRequest):
    # No authentication check
    gen = get_generator()
    article = gen.generate_wiki_article(...)
```

**Risks:**
- Anyone can consume your OpenAI credits
- No usage tracking per client
- No rate limiting
- Potential abuse

### Recommended: Add API Key Authentication

Here's how to add Bearer token authentication to protect your API:

#### Option 1: Simple API Key (Recommended for Development)

```python
# Add to src/web.py
from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os

# Initialize security
security = HTTPBearer()
API_KEYS = os.getenv("API_KEYS", "").split(",")  # Comma-separated keys

async def verify_api_key(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify API key from Bearer token."""
    if credentials.credentials not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Invalid or missing API key"
        )
    return credentials.credentials

# Protected endpoint example
@app.post("/generate/article")
async def generate_article(
    request: ArticleRequest,
    api_key: str = Security(verify_api_key)
):
    # Now requires valid API key
    gen = get_generator()
    article = gen.generate_wiki_article(...)
```

**Usage:**
```bash
# Add to .env
API_KEYS=your-secret-key-1,your-secret-key-2

# Client request
curl -X POST "http://localhost:8000/generate/article" \
  -H "Authorization: Bearer your-secret-key-1" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Muscat Festival", "language": "en"}'
```

#### Option 2: Database-Backed Authentication (Production)

```python
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

# User model with API keys
class APIKey(Base):
    __tablename__ = "api_keys"
    
    id = Column(Integer, primary_key=True)
    key = Column(String, unique=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime)
    is_active = Column(Boolean, default=True)
    rate_limit = Column(Integer, default=100)  # requests per hour

async def verify_api_key_db(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db)
):
    """Verify API key against database."""
    api_key = db.query(APIKey).filter(
        APIKey.key == credentials.credentials,
        APIKey.is_active == True,
        APIKey.expires_at > datetime.utcnow()
    ).first()
    
    if not api_key:
        raise HTTPException(status_code=401, detail="Invalid or expired API key")
    
    # Check rate limit
    if api_key.request_count_today >= api_key.rate_limit:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")
    
    return api_key
```

#### Option 3: JWT Authentication (Modern Apps)

```python
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"

async def verify_token(token: str = Depends(oauth2_scheme)):
    """Verify JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Deployment Recommendations

### For Render/Production:

1. **Add API Key Environment Variable:**
```yaml
# render.yaml
services:
  - type: web
    env: docker
    envVars:
      - key: OPENAI_API_KEY
        sync: false  # Set in Render dashboard
      - key: API_KEYS
        sync: false  # Comma-separated authorized keys
```

2. **Enable HTTPS Only:**
```python
# src/web.py
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

if os.getenv("ENVIRONMENT") == "production":
    app.add_middleware(HTTPSRedirectMiddleware)
```

3. **Add Rate Limiting:**
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.post("/generate/article")
@limiter.limit("10/minute")
async def generate_article(request: Request, ...):
    ...
```

## Current vs Secured API

### Current (No Auth):
```bash
curl -X POST "http://localhost:8000/generate/article" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Muscat Festival"}'
```

### With Bearer Token:
```bash
curl -X POST "http://localhost:8000/generate/article" \
  -H "Authorization: Bearer your-secret-api-key" \
  -H "Content-Type: application/json" \
  -d '{"event_name": "Muscat Festival"}'
```

## Quick Implementation

To add basic API key auth now:

1. **Update .env:**
```env
OPENAI_API_KEY=sk-svcacct-...
API_KEYS=dev-key-123,prod-key-456
```

2. **Add to requirements.txt:**
```txt
python-jose[cryptography]>=3.3.0
slowapi>=0.1.9
```

3. **Implement in web.py** (see Option 1 above)

## Summary

- **Current:** No authentication - anyone can use your API
- **OpenAI Key:** Safely stored in `.env`, not exposed
- **Recommendation:** Add Bearer token auth before production
- **Quick Fix:** Simple API key list in environment variables
- **Production:** Database-backed keys with rate limiting

For production deployment, authentication is **strongly recommended** to protect your OpenAI credits and prevent abuse.
