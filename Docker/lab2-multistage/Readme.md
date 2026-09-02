# 🚀 Multi-Stage Dockerized Full-Stack Application

This project demonstrates how to containerize a full-stack web application using a **multi-stage Docker build**. The backend is built with **Node.js**, while the frontend is served using **Nginx** in a lightweight production image.

---

## 📖 Project Overview

This Docker setup follows a **multi-stage build** approach to create an optimized production image.

- **Stage 1:** Builds the Node.js backend and installs all dependencies.
- **Stage 2:** Uses a lightweight Nginx image to serve the frontend while running the backend application.

This approach keeps the final image smaller, cleaner, and more production-ready by separating the build process from the runtime environment.

---

## 🛠️ Tech Stack

- 🟢 Node.js 22
- 🌐 Nginx (Alpine)
- 🐳 Docker
- 📦 Multi-Stage Docker Build

---

## 📂 Project Structure

```
.
├── Backend/
│   ├── package.json
│   ├── package-lock.json
│   ├── server.js
│   └── ...
│
├── Frontend/
│   ├── index.html
│   ├── nginx.conf
│   └── ...
│
├── Dockerfile
└── README.md
```

---

## 🏗️ Docker Build Stages

### 🔹 Stage 1 – Backend Build

- Uses the `node:22-alpine` image.
- Sets the working directory.
- Copies dependency files.
- Installs Node.js packages.
- Copies the backend source code.

---

### 🔹 Stage 2 – Production Image

- Uses the lightweight `nginx:alpine` image.
- Copies frontend files into the Nginx web root.
- Replaces the default Nginx configuration.
- Copies the backend application from Stage 1.
- Installs Node.js to run the backend.
- Starts both the backend server and Nginx.

---

## 🚀 Build the Docker Image

```bash
docker build -t fullstack-app .
```

---

## ▶️ Run the Container

```bash
docker run -d -p 80:80 --name fullstack-app fullstack-app
```

---

## 🌐 Access the Application

Open your browser and visit:

```
http://localhost
```

If deployed on a cloud server (AWS EC2, GCP VM, Azure VM, etc.):

```
http://<YOUR_PUBLIC_IP>
```

---

## 🛑 Stop and Remove the Container

Stop the running container:

```bash
docker stop fullstack-app
```

Remove the container:

```bash
docker rm fullstack-app
```

---

## 💡 Concepts Practiced

- Multi-Stage Docker Builds
- Docker Image Optimization
- Containerizing a Node.js Backend
- Serving Static Files with Nginx
- Running Multiple Processes in a Single Container
- Docker Image Layer Caching
- Production Image Creation

---

## 📚 Learning Outcomes

Through this project, I learned:

- How multi-stage Docker builds reduce image size.
- How to separate the build and production stages.
- How to combine a Node.js backend with an Nginx frontend.
- How Docker caches layers to speed up future builds.
- How to deploy a production-ready container.

---

## 👩‍💻 Author

**Ishika Sharma**

- 🌐 Portfolio: https://ishikasharma05.github.io/ishikasharma.github.io/
- 💼 LinkedIn: https://www.linkedin.com/in/ishika-sharma-connect/
- 💻 GitHub: https://github.com/ishikasharma05

---

⭐ If you found this project helpful, feel free to star the repository and connect with me on LinkedIn!
