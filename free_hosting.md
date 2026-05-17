# 🚀 Free Hosting Stack Setup

This project is fully deployed using free-tier cloud services.

---

# 🌐 Frontend Hosting

## Vercel

Used for hosting the React frontend application.

### Tech
- React
- Vite
- TypeScript

### Features
- Automatic deployments from GitHub
- Free SSL
- Global CDN
- Fast frontend hosting

### Website
https://vercel.com

---

# ⚡ Backend Hosting

## Render

Used for hosting the FastAPI backend.

### Tech
- FastAPI
- Uvicorn
- Python

### Features
- Free web service hosting
- Automatic GitHub deployment
- Environment variable support
- HTTPS enabled

### Website
https://render.com

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

# 🐘 PostgreSQL Database

## Neon

Used for managed PostgreSQL database hosting.

### Features
- Serverless PostgreSQL
- Free tier available
- SSL support
- Easy connection string management

### Website
https://neon.tech

---

# 🔴 Redis Hosting

## Upstash

Used for Redis caching and session management.

### Features
- Serverless Redis
- REST + TCP support
- Free tier
- Global edge network

### Website
https://upstash.com

---

# 🐇 RabbitMQ Hosting

## CloudAMQP

Used for RabbitMQ message queue hosting.

### Features
- Managed RabbitMQ
- Free "Little Lemur" plan
- AMQP protocol support
- Queue monitoring dashboard

### Website
https://www.cloudamqp.com

---

# 🔐 Environment Variables

## Backend (.env)

```env
APP_NAME=MyApp
APP_ENV=production
DEBUG=False
PORT=8000

DATABASE_URL=postgresql+asyncpg://...

REDIS_URL=redis://...

RABBITMQ_URL=amqps://...

JWT_SECRET_KEY=your_secret
JWT_ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

---

# 🌍 Deployment Flow

## Frontend

GitHub → Vercel → Live React App

## Backend

GitHub → Render → Live FastAPI API

## Database

FastAPI ↔ Neon PostgreSQL

## Redis

FastAPI ↔ Upstash Redis

## Queue System

FastAPI ↔ CloudAMQP RabbitMQ

---

# ✅ Production Notes

- Use HTTPS URLs only
- Add frontend domain to backend CORS
- Store secrets in environment variables
- Never commit `.env` files to GitHub
- Use SSL-enabled database connections
- Disable debug mode in production

---

# 🔥 Recommended Future Improvements

- Add Docker support
- Configure CI/CD pipeline
- Add monitoring/logging
- Add rate limiting
- Use custom domains
- Configure automated backups
- Add centralized error tracking
- Add API versioning
- Add health monitoring endpoints

---

# 📦 Tech Stack Summary

| Service | Provider |
|---|---|
| Frontend Hosting | Vercel |
| Backend Hosting | Render |
| PostgreSQL Database | Neon |
| Redis | Upstash |
| RabbitMQ | CloudAMQP |
| Backend Framework | FastAPI |
| Frontend Framework | React + Vite |
| ORM | SQLAlchemy |
| Authentication | JWT |
| Queue System | RabbitMQ |
| Cache Layer | Redis |

---

# 🚀 Current Architecture

```text
React Frontend (Vercel)
        ↓
FastAPI Backend (Render)
        ↓
 ┌───────────────┬───────────────┬───────────────┐
 ↓               ↓               ↓
Neon         Upstash        CloudAMQP
PostgreSQL     Redis         RabbitMQ
```

---

# 🔒 Security Notes

- JWT authentication enabled
- Password hashing enabled
- CORS configured
- SSL-enabled database connections
- Environment-based configuration
- Refresh token support
- Session management enabled
- Device tracking enabled

---