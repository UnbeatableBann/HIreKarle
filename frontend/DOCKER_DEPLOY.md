# Frontend Docker Deployment

## Development Deployment

**File:** `Dockerfile`

### Build and Run
```bash
cd frontend

# Build image
docker build -t hirekarle-frontend .

# Run container
docker run -p 3000:3000 hirekarle-frontend
```

**Access:** http://localhost:3000

---

## Production Deployment

**File:** `Dockerfile.prod`

### Build and Run
```bash
cd frontend

# Build image
docker build -f Dockerfile.prod -t hirekarle-frontend-prod .

# Run container
docker run -p 80:80 hirekarle-frontend-prod
```

**Access:** http://localhost

---

## With Environment Variables

### Development
```bash
docker run -p 3000:3000 \
  -e REACT_APP_API_BASE_URL=http://backend:8000 \
  hirekarle-frontend
```

### Production
```bash
# Build with custom API URL
docker build -f Dockerfile.prod \
  --build-arg REACT_APP_API_BASE_URL=https://api.yourdomain.com \
  -t hirekarle-frontend-prod .

docker run -p 80:80 hirekarle-frontend-prod
```

---

## Docker Compose

See `docker-compose.yml` in root directory for full stack deployment.

```bash
cd ..
docker-compose up
```
