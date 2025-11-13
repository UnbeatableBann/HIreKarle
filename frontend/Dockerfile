# -------- Stage 1: Build --------
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install --legacy-peer-deps

# Copy all project files and build
COPY . .
RUN npm run build

# -------- Stage 2: Deploy with Nginx --------
FROM nginx:stable-alpine

# Copy React build to Nginx HTML directory
COPY --from=builder /app/build /usr/share/nginx/html

# Expose default HTTP port
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
