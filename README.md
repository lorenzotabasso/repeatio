# Repeatio

One day, **a friend of mine asked me** if I knew of a **quick and smart way** to get an **audio track to listen to and repeat in order to learn a foreign language** (at least the basics). I replied that I didn't know of any such software, but that if he gave me some time, **I could create it for him**. And that's how **Repetio was born**.

*Modern language learning with repetition.* Nx monorepo with **Next.js** frontend and **FastAPI** backend.

- Frontend docs: `apps/frontend/README.md`
- Backend docs: `apps/backend/README.md`

## Quick Start

### Using Docker (recommended)

```bash
git clone https://github.com/lorenzotabasso/repeatio.git &&
cd repeatio &&
docker compose up -d --build &&
docker compose logs -f
```

### Local run

#### Manually without Docker

```bash
# Backend
cd apps/backend && pip install -r requirements.txt && python main.py

# Frontend
cd apps/frontend && npm install && npm run dev
```

#### Using Nx

```bash
npm install &&
nx serve backend && 
nx serve frontend &&
```

## Access

- **Frontend**: [http://localhost:3000](http://localhost:3000)
- **Backend API**: [http://localhost:8000](http://localhost:8000)
- **API Docs (OpenAPI)**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Useful Commands

### Root (workspace)

```bash
# Docker lifecycle
npm run docker:build
npm run docker:up
npm run docker:down
npm run docker:build-all
npm run docker:logs

# Nx workspace scripts
npm run build
npm run serve
npm run dev
npm run test
npm run lint
```

### Per app (using Nx)

```bash
# Frontend
nx serve frontend
nx build frontend
nx lint frontend

# Backend
nx serve backend
nx lint backend
```

## API (essentials)

- POST `/api/v1/audio/csv-to-audio` – CSV to audio
- POST `/api/v1/audio/text-to-audio` – Single text to audio
- GET `/api/v1/audio/files` – List files
- GET `/api/v1/audio/download/{filename}` – Download
- DELETE `/api/v1/audio/files/{filename}` – Delete

See full reference at [http://localhost:8000/docs](http://localhost:8000/docs)

## Enviroment configs

- Frontend: `NEXT_PUBLIC_API_URL` (default [http://localhost:8000](http://localhost:8000))
- Backend: `UPLOAD_DIR`, `OUTPUT_DIR`, `DEFAULT_PAUSE_DURATION`, `DEFAULT_SILENCE_DURATION`

## Troubleshooting (quick)

```bash
# Ports busy
lsof -i :3000; lsof -i :8000
docker compose down

# Rebuild without cache
docker compose build --no-cache

# Logs / status
docker compose logs -f
docker compose ps
```

## License & Contributing

MIT. See `LICENSE`. PRs welcome.
