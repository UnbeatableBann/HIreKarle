# HireKarle Deployment Guide

## 🚀 Production Deployment Options

### Option 1: AWS Deployment

#### Architecture
```
CloudFront (CDN)
    ↓
S3 (Frontend) + API Gateway
    ↓
EC2/ECS (Backend)
    ↓
ElastiCache (Redis)
```

#### Steps

**1. Backend on EC2**
```bash
# Launch EC2 instance (t3.medium recommended)
# SSH into instance
ssh -i key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install python3 git redis -y

# Clone repository
git clone https://github.com/yourusername/hirekarle.git
cd hirekarle/backend

# Setup Python environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
nano .env  # Add production values

# Install and configure Nginx
sudo yum install nginx -y
sudo nano /etc/nginx/conf.d/hirekarle.conf
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Setup Systemd Service:**
```bash
sudo nano /etc/systemd/system/hirekarle.service
```

```ini
[Unit]
Description=HireKarle API
After=network.target

[Service]
User=ec2-user
WorkingDirectory=/home/ec2-user/hirekarle/backend
Environment="PATH=/home/ec2-user/hirekarle/backend/venv/bin"
ExecStart=/home/ec2-user/hirekarle/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable hirekarle
sudo systemctl start hirekarle
```

**2. Redis on ElastiCache**
```bash
# Create ElastiCache Redis cluster
# Update .env with ElastiCache endpoint
REDIS_HOST=your-cluster.cache.amazonaws.com
REDIS_PORT=6379
```

**3. Frontend on S3 + CloudFront**
```bash
cd frontend

# Build production bundle
npm run build

# Upload to S3
aws s3 sync build/ s3://your-bucket-name --delete

# Configure CloudFront distribution
# Point to S3 bucket
# Enable HTTPS with ACM certificate
```

---

### Option 2: Google Cloud Platform

#### Architecture
```
Cloud CDN
    ↓
Cloud Storage (Frontend) + Cloud Run (Backend)
    ↓
Memorystore (Redis)
```

#### Steps

**1. Backend on Cloud Run**
```bash
# Build and push Docker image
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/hirekarle-backend

# Deploy to Cloud Run
gcloud run deploy hirekarle-backend \
  --image gcr.io/PROJECT_ID/hirekarle-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GEMINI_API_KEY=your_key,REDIS_HOST=your_redis_ip
```

**2. Redis on Memorystore**
```bash
gcloud redis instances create hirekarle-redis \
  --size=1 \
  --region=us-central1 \
  --redis-version=redis_6_x
```

**3. Frontend on Cloud Storage**
```bash
cd frontend
npm run build

gsutil -m rsync -r build/ gs://your-bucket-name
gsutil web set -m index.html -e index.html gs://your-bucket-name
```

---

### Option 3: Docker Compose (VPS)

For DigitalOcean, Linode, or any VPS:

```bash
# Install Docker and Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Clone repository
git clone https://github.com/yourusername/hirekarle.git
cd hirekarle

# Configure environment
cp backend/.env.example backend/.env
nano backend/.env

# Start services
docker-compose up -d

# Setup Nginx reverse proxy
sudo apt install nginx -y
sudo nano /etc/nginx/sites-available/hirekarle
```

**Nginx Config:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
}
```

---

### Option 4: Vercel (Frontend) + Railway (Backend)

**Frontend on Vercel:**
```bash
cd frontend
vercel --prod
```

**Backend on Railway:**
1. Connect GitHub repository
2. Select backend folder
3. Add environment variables
4. Deploy automatically

---

## 🔒 Production Checklist

### Security
- [ ] Enable HTTPS (Let's Encrypt/ACM)
- [ ] Set strong Redis password
- [ ] Configure CORS properly
- [ ] Add rate limiting
- [ ] Enable API authentication (optional)
- [ ] Set up firewall rules
- [ ] Regular security updates

### Performance
- [ ] Enable Redis persistence
- [ ] Configure CDN for frontend
- [ ] Set up caching headers
- [ ] Optimize Docker images
- [ ] Enable gzip compression
- [ ] Monitor API response times

### Monitoring
- [ ] Set up CloudWatch/Stackdriver logs
- [ ] Configure error tracking (Sentry)
- [ ] Monitor Redis memory usage
- [ ] Track Gemini API costs
- [ ] Set up uptime monitoring
- [ ] Configure alerts

### Backup
- [ ] Redis backup strategy
- [ ] Application logs retention
- [ ] Database snapshots (if added)

---

## 📊 Scaling Strategies

### Horizontal Scaling
```yaml
# docker-compose.yml for multiple backend instances
services:
  backend:
    deploy:
      replicas: 3
    
  nginx:
    image: nginx
    depends_on:
      - backend
```

### Load Balancing
- Use AWS ALB / GCP Load Balancer
- Configure health checks
- Enable sticky sessions if needed

### Redis Scaling
- Use Redis Cluster for high availability
- Configure read replicas
- Implement Redis Sentinel

---

## 🔧 Environment Variables (Production)

```env
# Backend (.env)
GEMINI_API_KEY=your_production_key
REDIS_HOST=production-redis-host
REDIS_PORT=6379
REDIS_PASSWORD=strong_password_here
SESSION_TTL=604800
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Optional
SENTRY_DSN=your_sentry_dsn
LOG_LEVEL=INFO
MAX_UPLOAD_SIZE=10485760
```

---

## 🐛 Troubleshooting

### Backend won't start
```bash
# Check logs
docker-compose logs backend

# Verify environment variables
docker-compose exec backend env | grep GEMINI

# Test Redis connection
docker-compose exec backend python -c "import redis; r=redis.Redis(host='redis'); print(r.ping())"
```

### High memory usage
```bash
# Check Redis memory
redis-cli INFO memory

# Clear old sessions
redis-cli --scan --pattern "resume:*" | xargs redis-cli DEL
```

### Slow API responses
- Check Gemini API rate limits
- Monitor Redis latency
- Review application logs
- Optimize job scraping concurrency

---

## 💰 Cost Estimation

### AWS (Monthly)
- EC2 t3.medium: ~$30
- ElastiCache (1GB): ~$15
- S3 + CloudFront: ~$5
- **Total: ~$50/month**

### GCP (Monthly)
- Cloud Run: ~$20
- Memorystore (1GB): ~$25
- Cloud Storage: ~$5
- **Total: ~$50/month**

### VPS (Monthly)
- DigitalOcean Droplet (2GB): $12
- **Total: ~$12/month**

**Plus:**
- Gemini API: Pay per use (~$0.001/request)
- Domain: ~$12/year
- SSL: Free (Let's Encrypt)

---

## 📈 Monitoring Dashboard

Recommended tools:
- **Grafana**: Visualize metrics
- **Prometheus**: Collect metrics
- **Sentry**: Error tracking
- **Uptime Robot**: Uptime monitoring

---

## 🔄 CI/CD Pipeline

**GitHub Actions Example:**
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Deploy Backend
        run: |
          ssh user@server 'cd hirekarle && git pull && docker-compose up -d --build'
      
      - name: Deploy Frontend
        run: |
          cd frontend
          npm install
          npm run build
          aws s3 sync build/ s3://your-bucket
```

---

## 📞 Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Check GitHub issues
4. Contact support

---

## 🎯 Post-Deployment

1. Test all endpoints
2. Monitor for 24 hours
3. Set up alerts
4. Document any custom configurations
5. Create backup/restore procedures
