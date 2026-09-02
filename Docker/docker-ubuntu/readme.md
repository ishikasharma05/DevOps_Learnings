# Dockerized Nginx Static Website

This project uses Docker to serve a static HTML page with Nginx on an Ubuntu base image.

## Prerequisites

- Docker installed on your system

## Project Structure

```
.
├── Dockerfile
├── index.html
└── README.md
```

## Dockerfile Overview

- Uses the latest Ubuntu image.
- Updates package lists.
- Installs Nginx.
- Removes the default Nginx web page.
- Copies `index.html` as the new homepage.
- Exposes port `80`.
- Starts Nginx in the foreground.

## Build the Docker Image

```bash
docker build -t nginx-static-site .
```

## Run the Container

```bash
docker run -d -p 8080:80 --name my-nginx-site nginx-static-site
```

## Access the Website

Open your browser and visit:

```
http://localhost:8080
```

You should see the contents of your `index.html` file.

## Stop and Remove the Container

```bash
docker stop my-nginx-site
docker rm my-nginx-site
```

## Author

Ishika Sharma
