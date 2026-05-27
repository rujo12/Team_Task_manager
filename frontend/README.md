# Team Task Manager Frontend

React + Vite frontend for the Team Task Manager application.

## Stack

- React
- Vite
- Tailwind CSS
- Axios
- React Router

## Features

- JWT authentication flow (signup/login/logout)
- Persistent session with token refresh handling
- Protected routes
- Role-aware UI for `ADMIN` / `MEMBER`
- Dashboard statistics view
- Projects management (list/create/add member)
- Tasks management (list/create/update status)
- Responsive, minimal UI

## Environment Variables

Create `.env` from `.env.example`:

```bash
cp .env.example .env
```

```env
VITE_API_BASE_URL=http://127.0.0.1:8000
```

## Run Locally

```bash
cd frontend
npm install
npm run dev
```

Frontend runs on `http://localhost:5173` by default.

## Build

```bash
npm run build
npm run preview
```

## Deployment (Vercel)

- `vercel.json` is configured for SPA route rewrites.
- Set `VITE_API_BASE_URL` in Vercel environment variables.
