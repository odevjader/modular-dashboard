# frontend/Dockerfile

# --- Stage 1: Build the React application ---
FROM node:20-alpine as builder

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json (or yarn.lock)
COPY package.json package-lock.json* ./
# If using yarn:
# COPY package.json yarn.lock ./

# Install dependencies
RUN npm install
# If using yarn:
# RUN yarn install

# Copy the rest of the application code
COPY . .

# Build the application for production
# This command runs the 'build' script defined in package.json
# Output is usually placed in a 'dist' folder by Vite
RUN npm run build
# If using yarn:
# RUN yarn build


# --- Stage 2: Serve the application using Nginx ---
FROM nginx:1.25-alpine

# Copy the build output from the builder stage to Nginx's web server directory
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy custom Nginx configuration (optional but recommended for SPAs)
# We'll create this nginx.conf file next if needed, or use a default approach first.
# For SPAs (Single Page Applications) like React, Nginx needs to be configured
# to redirect all non-file requests to index.html to let React Router handle routing.

# Create a basic Nginx config that supports SPA routing
RUN echo "\
server { \n\
    listen 80; \n\
    server_name localhost; \n\
    \n\
    root /usr/share/nginx/html; \n\
    index index.html index.htm; \n\
    \n\
    location / { \n\
        # Try serving the requested file, then directory, then fallback to index.html \n\
        try_files \$uri \$uri/ /index.html; \n\
    } \n\
    \n\
    # Optional: Configure error pages \n\
    error_page 500 502 503 504 /50x.html; \n\
    location = /50x.html { \n\
        root /usr/share/nginx/html; \n\
    } \n\
} \
" > /etc/nginx/conf.d/default.conf


# Expose port 80 (standard HTTP port Nginx listens on)
EXPOSE 80

# Command to start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]