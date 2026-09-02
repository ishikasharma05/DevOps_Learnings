########################################################
# STAGE 1 - Build the Backend Application
########################################################

# Use Node.js Alpine image as the base image
FROM node:22-alpine AS backend

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json first
# This helps Docker cache the npm install layer
COPY Backend/package*.json ./

# Install backend dependencies
RUN npm install

# Copy the remaining backend source code
COPY Backend/ .

########################################################
# STAGE 2 - Create the Final Production Image
########################################################

# Start with a lightweight Nginx image
FROM nginx:alpine

# Copy all frontend files into Nginx's web root
COPY Frontend/ /usr/share/nginx/html/

# Replace the default Nginx configuration
COPY Frontend/nginx.conf /etc/nginx/conf.d/default.conf

# Copy the backend application from Stage 1
# We don't rebuild it—we simply reuse the files
COPY --from=backend /app /backend

# Install Node.js because the backend needs it to run
RUN apk add --no-cache nodejs

# Set the working directory for the backend
WORKDIR /backend

# Expose port 80 for the web application
EXPOSE 80

# Start both the Node.js backend and Nginx
CMD sh -c "node server.js & nginx -g 'daemon off;'"