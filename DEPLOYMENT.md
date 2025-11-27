# Deployment Guide

This guide covers deploying the Oman Wikipedia Generator to various platforms.

## Table of Contents

- [Docker Deployment](#docker-deployment)
- [Heroku Deployment](#heroku-deployment)
- [Azure App Service](#azure-app-service)
- [AWS Deployment](#aws-deployment)
- [Environment Variables](#environment-variables)

## Docker Deployment

### Local Docker

Build and run locally:

```bash
# Build image
docker build -t oman-wiki-generator .

# Run CLI
docker run --rm -e OPENAI_API_KEY=your_key oman-wiki-generator \
  python -m src.cli article "Muscat Festival"

# Run web interface
docker run -p 8000:8000 --target web \
  -e OPENAI_API_KEY=your_key oman-wiki-generator
```

### Docker Compose

```bash
# Set environment variables in .env file
cp .env.example .env
# Edit .env and add your API key

# Start services
docker-compose up

# Run specific service
docker-compose up wiki-web

# Run tests
docker-compose run test
```

### Docker Hub

```bash
# Tag image
docker tag oman-wiki-generator moodi112/oman-wiki-generator:latest

# Push to Docker Hub
docker push moodi112/oman-wiki-generator:latest

# Pull and run
docker pull moodi112/oman-wiki-generator:latest
docker run -p 8000:8000 moodi112/oman-wiki-generator:latest
```

## Heroku Deployment

### Prerequisites

- Heroku CLI installed
- Heroku account

### Steps

1. **Login to Heroku**
```bash
heroku login
```

2. **Create Heroku app**
```bash
heroku create oman-wiki-generator
```

3. **Set environment variables**
```bash
heroku config:set OPENAI_API_KEY=your_actual_api_key
heroku config:set OPENAI_MODEL=gpt-4
```

4. **Deploy via Git**
```bash
git push heroku main
```

5. **Deploy via Container Registry**
```bash
# Login to container registry
heroku container:login

# Build and push
heroku container:push web -a oman-wiki-generator

# Release
heroku container:release web -a oman-wiki-generator
```

6. **Open app**
```bash
heroku open
```

### One-Click Deploy

[![Deploy to Heroku](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

The `app.json` file configures automatic deployment with required environment variables.

## Azure App Service

### Prerequisites

- Azure CLI installed
- Azure account

### Steps

1. **Login to Azure**
```bash
az login
```

2. **Create resource group**
```bash
az group create --name oman-wiki-rg --location eastus
```

3. **Create App Service plan**
```bash
az appservice plan create \
  --name oman-wiki-plan \
  --resource-group oman-wiki-rg \
  --sku B1 \
  --is-linux
```

4. **Create web app**
```bash
az webapp create \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --plan oman-wiki-plan \
  --runtime "PYTHON|3.11"
```

5. **Configure startup command**
```bash
az webapp config set \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --startup-file "uvicorn src.web:app --host 0.0.0.0 --port 8000"
```

6. **Set environment variables**
```bash
az webapp config appsettings set \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --settings OPENAI_API_KEY=your_key OPENAI_MODEL=gpt-4
```

7. **Deploy code**
```bash
# Via ZIP deploy
az webapp deployment source config-zip \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --src ./deploy.zip

# Or via Git
az webapp deployment source config \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --repo-url https://github.com/moodi112/https-github.com-moodi112-moodi112 \
  --branch main
```

### Docker Container on Azure

```bash
# Create container-based web app
az webapp create \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --plan oman-wiki-plan \
  --deployment-container-image-name moodi112/oman-wiki-generator:latest

# Configure
az webapp config appsettings set \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --settings OPENAI_API_KEY=your_key
```

## AWS Deployment

### AWS Elastic Beanstalk

1. **Install EB CLI**
```bash
pip install awsebcli
```

2. **Initialize EB**
```bash
eb init -p python-3.11 oman-wiki-generator
```

3. **Create environment**
```bash
eb create oman-wiki-env
```

4. **Set environment variables**
```bash
eb setenv OPENAI_API_KEY=your_key OPENAI_MODEL=gpt-4
```

5. **Deploy**
```bash
eb deploy
```

6. **Open application**
```bash
eb open
```

### AWS ECS (Docker)

1. **Create ECR repository**
```bash
aws ecr create-repository --repository-name oman-wiki-generator
```

2. **Build and push image**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | \
  docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build
docker build -t oman-wiki-generator .

# Tag
docker tag oman-wiki-generator:latest \
  <account-id>.dkr.ecr.us-east-1.amazonaws.com/oman-wiki-generator:latest

# Push
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/oman-wiki-generator:latest
```

3. **Create ECS task definition and service** via AWS Console or CLI

### AWS Lambda (Serverless)

For lightweight API operations:

```bash
# Install Zappa
pip install zappa

# Initialize
zappa init

# Deploy
zappa deploy production

# Update
zappa update production
```

## Environment Variables

### Required

- `OPENAI_API_KEY` - Your OpenAI API key

### Optional

- `OPENAI_MODEL` - Model to use (default: gpt-4)
- `PORT` - Port for web server (default: 8000)

### Setting Environment Variables

**Docker:**
```bash
docker run -e OPENAI_API_KEY=key -e OPENAI_MODEL=gpt-4 ...
```

**Docker Compose:**
```yaml
environment:
  - OPENAI_API_KEY=${OPENAI_API_KEY}
  - OPENAI_MODEL=${OPENAI_MODEL}
```

**Heroku:**
```bash
heroku config:set OPENAI_API_KEY=key
```

**Azure:**
```bash
az webapp config appsettings set --settings OPENAI_API_KEY=key
```

**AWS EB:**
```bash
eb setenv OPENAI_API_KEY=key
```

## Health Checks

All deployments should configure health checks:

**Endpoint:** `/health`

**Expected Response:**
```json
{
  "status": "healthy",
  "service": "oman-wiki-generator"
}
```

## Scaling

### Horizontal Scaling

- **Heroku:** `heroku ps:scale web=3`
- **Azure:** Adjust App Service Plan or use Auto-scale
- **AWS:** Configure Auto Scaling Groups
- **Docker:** Use Docker Swarm or Kubernetes

### Vertical Scaling

- Upgrade to higher-tier plans
- Increase container resources
- Use more powerful instance types

## Monitoring

### Application Insights (Azure)

```bash
az webapp log config \
  --name oman-wiki-generator \
  --resource-group oman-wiki-rg \
  --application-logging true
```

### CloudWatch (AWS)

Automatically configured with ECS/EB deployments.

### Heroku Logs

```bash
heroku logs --tail
```

### Docker Logs

```bash
docker logs <container-id>
docker-compose logs -f
```

## Security Best Practices

1. **Never commit API keys** - Use environment variables
2. **Enable HTTPS** - All platforms support automatic SSL
3. **Set CORS policies** - Configure in `src/web.py`
4. **Rate limiting** - Implement for production
5. **API key rotation** - Regularly update OpenAI keys
6. **Security scanning** - Use Bandit (included in CI)
7. **Dependency updates** - Keep requirements.txt current

## Cost Optimization

1. **Use appropriate instance sizes** - Start small, scale as needed
2. **Implement caching** - Cache common API responses
3. **Use cheaper models** - Consider gpt-3.5-turbo for non-critical tasks
4. **Auto-scaling** - Scale down during low traffic
5. **Optimize Docker images** - Use multi-stage builds (included)

## Troubleshooting

### Container Won't Start

Check logs:
```bash
docker logs <container-id>
heroku logs --tail
az webapp log tail
```

### API Key Errors

Verify environment variable:
```bash
# Heroku
heroku config

# Azure
az webapp config appsettings list

# Docker
docker exec <container-id> env | grep OPENAI
```

### Port Binding Issues

Ensure app listens on correct port (PORT environment variable).

### Memory Issues

Increase container/instance memory limits or upgrade tier.

## Support

For deployment issues:
- Check platform-specific documentation
- Review application logs
- Verify environment variables
- Test locally with Docker first
- Open GitHub issue with deployment details
