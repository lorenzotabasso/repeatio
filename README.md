# Repeatio

A modern language learning application that leverages the power of repetition for effective learning. Built with **Nx Monorepo**, **React/Next.js Frontend**, and **FastAPI Backend**.

<a alt="Nx logo" href="https://nx.dev" target="_blank" rel="noreferrer"><img src="https://raw.githubusercontent.com/nrwl/nx/master/images/nx-logo.png" width="45"></a>

## 🚀 Features

- **Multi-language Audio Generation**: Convert CSV files with sentences to audio files
- **10 Supported Languages**: Italian, Russian, English, Spanish, French, German, Portuguese, Japanese, Korean, Chinese
- **Modern Web Interface**: Beautiful React/Next.js frontend with real-time progress tracking
- **RESTful API**: FastAPI backend with comprehensive endpoints
- **Docker Integration**: Full containerization for easy deployment
- **Nx Monorepo**: Efficient development workflow with shared tooling

## 🏗️ Architecture

```
repeatio/
├── apps/
│   ├── frontend/          # Next.js React application
│   └── backend/           # FastAPI Python application
├── docker-compose.yml     # Unified Docker setup
└── project.json          # Nx workspace configuration
```

## 🛠️ Prerequisites

- **Docker & Docker Compose**
- **Node.js 18+** (for Nx commands)
- **Python 3.11+** (for local backend development)

## 🚀 Quick Start

### Option 1: Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd repeatio

# Build and start all services
docker compose build --no-cache
docker compose up -d

# View logs
docker compose logs -f
```

### Option 2: Nx Commands

```bash
# Install dependencies
npm install

# Start both frontend and backend
npm run dev

# Or use individual commands
nx serve frontend
nx serve backend
```

## 📖 Available Commands

### 🐳 Docker Commands

#### Root Level (Nx Workspace)
```bash
# Build all containers
npm run docker:build

# Start all services
npm run docker:up

# Stop all services
npm run docker:down

# Rebuild all containers
npm run docker:build-all

# View logs
npm run docker:logs
```

#### Individual Services
```bash
# Frontend only
nx docker-build frontend
nx docker-run frontend

# Backend only
nx docker-build backend
nx docker-run backend
nx docker-compose-up backend
nx docker-compose-down backend
```

### 🏗️ Development Commands

#### Root Level
```bash
# Build both applications
npm run build

# Serve both applications in development
npm run serve

# Development mode (parallel)
npm run dev

# Run tests/linting
npm run test
npm run lint
```

#### Individual Applications
```bash
# Frontend
nx serve frontend
nx build frontend
nx lint frontend

# Backend
nx serve backend
nx lint backend
```

### 🔧 Docker Compose Commands

```bash
# Build and start
docker compose up -d

# Stop services
docker compose down

# Rebuild containers
docker compose build --no-cache

# View logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 📋 API Endpoints

### Audio Generation
- `POST /api/v1/audio/csv-to-audio` - Convert CSV to audio
- `POST /api/v1/audio/text-to-audio` - Convert single text to audio
- `GET /api/v1/audio/download/{filename}` - Download generated audio
- `GET /api/v1/audio/files` - List generated files
- `DELETE /api/v1/audio/files/{filename}` - Delete audio file

### System
- `GET /api/v1/audio/health` - Health check with system info
- `GET /api/v1/audio/supported-languages` - List supported languages

## 📁 Project Structure

```
repeatio/
├── apps/
│   ├── frontend/
│   │   ├── src/
│   │   │   └── app/
│   │   │       └── page.tsx          # Main UI component
│   │   ├── Dockerfile
│   │   └── project.json
│   └── backend/
│       ├── src/
│       │   ├── api/
│       │   │   └── audio.py          # API routes
│       │   ├── models/
│       │   │   └── audio.py          # Pydantic models
│       │   ├── services/
│       │   │   └── audio_service.py  # Business logic
│       │   └── core/
│       │       └── config.py         # Configuration
│       ├── main.py                    # FastAPI app
│       ├── Dockerfile
│       └── project.json
├── docker-compose.yml                 # Unified Docker setup
├── project.json                       # Root Nx configuration
└── package.json                       # Root dependencies
```

## 🔧 Configuration

### Environment Variables

#### Frontend
- `NEXT_PUBLIC_API_URL` - Backend API URL (default: http://localhost:8000)

#### Backend
- `UPLOAD_DIR` - Directory for uploaded files (default: uploads)
- `OUTPUT_DIR` - Directory for generated audio (default: outputs)
- `DEFAULT_PAUSE_DURATION` - Pause between languages in ms (default: 5000)
- `DEFAULT_SILENCE_DURATION` - Silence between sentences in ms (default: 1000)

### Supported Languages

| Code | Language | Flag |
|------|----------|------|
| `it` | Italian | 🇮🇹 |
| `ru` | Russian | 🇷🇺 |
| `en` | English | 🇺🇸 |
| `es` | Spanish | 🇪🇸 |
| `fr` | French | 🇫🇷 |
| `de` | German | 🇩🇪 |
| `pt` | Portuguese | 🇵🇹 |
| `ja` | Japanese | 🇯🇵 |
| `ko` | Korean | 🇰🇷 |
| `zh` | Chinese | 🇨🇳 |

## 📝 Usage

### 1. Prepare CSV File
Create a CSV file with sentences in different languages:
```csv
Hello world,Bonjour le monde
Good morning,Buongiorno
Thank you,Grazie
```

### 2. Upload and Process
1. Open http://localhost:3000
2. Select your CSV file
3. Choose languages for each column
4. Click "Start Audio Generation"
5. Download the generated audio file

### 3. API Usage
```bash
# Convert CSV to audio
curl -X POST http://localhost:8000/api/v1/audio/csv-to-audio \
  -F "csv_file=@sentences.csv" \
  -F 'request={"languages":[{"column_index":0,"language_code":"en","flag":"🇺🇸"},{"column_index":1,"language_code":"fr","flag":"🇫🇷"}],"output_filename":"output.mp3"}'

# Convert single text
curl -X POST http://localhost:8000/api/v1/audio/text-to-audio \
  -H "Content-Type: application/json" \
  -d '{"text":"Hello world","language":"en","output_filename":"hello.mp3"}'
```

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the port
   lsof -i :3000
   lsof -i :8000
   
   # Stop conflicting services
   docker compose down
   ```

2. **Docker build fails**
   ```bash
   # Clean Docker cache
   docker system prune -a
   
   # Rebuild without cache
   docker compose build --no-cache
   ```

3. **Frontend can't connect to backend**
   - Check if backend is running: `docker compose ps`
   - Verify CORS settings in backend
   - Check network connectivity between containers

4. **Audio generation fails**
   - Ensure FFmpeg is available in container
   - Check CSV file format
   - Verify language codes are supported

### Logs and Debugging

```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f frontend

# Check container status
docker compose ps

# Access container shell
docker compose exec backend bash
docker compose exec frontend sh
```

## 🧪 Development

### Local Development (without Docker)

```bash
# Frontend
cd apps/frontend
npm install
npm run dev

# Backend
cd apps/backend
pip install -r requirements.txt
python main.py
```

### Adding New Features

1. **Frontend**: Add components in `apps/frontend/src/app/`
2. **Backend**: Add routes in `apps/backend/src/api/`
3. **Models**: Update `apps/backend/src/models/`
4. **Services**: Add business logic in `apps/backend/src/services/`

### Testing

```bash
# Run all tests
npm run test

# Lint code
npm run lint

# Type checking
nx typecheck frontend
```

## 📄 License

MIT License - see LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue in the repository
- Check the troubleshooting section above
- Review the API documentation at http://localhost:8000/docs

---

Built with ❤️ using [Nx](https://nx.dev), [Next.js](https://nextjs.org), and [FastAPI](https://fastapi.tiangolo.com/).
