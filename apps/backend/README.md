# Audio Microservice

A FastAPI-based microservice for converting text to audio using Google Text-to-Speech (gTTS) and processing CSV files with multiple language sentences.

## Features

- **Text to Audio**: Convert single text strings to audio files
- **CSV to Audio**: Process CSV files with multiple language sentences
- **Multiple Language Support**: Support for 10+ languages including Italian, Russian, English, Spanish, French, German, Portuguese, Japanese, Korean, and Chinese
- **File Management**: Upload, download, and manage generated audio files
- **Health Monitoring**: Check service health and FFmpeg availability
- **RESTful API**: Clean REST API with automatic OpenAPI documentation

## Prerequisites

### FFmpeg and FFprobe Installation

**Important**: This service requires both `ffmpeg` and `ffprobe` to be installed. Most FFmpeg installations include both tools, but some minimal installations might only include `ffmpeg`. The service will check for both tools on startup and provide clear error messages if either is missing.

This service requires **both FFmpeg and FFprobe** to be installed on your system. FFprobe is typically included with FFmpeg installations.

**macOS:**
```bash
# Using Homebrew (includes both ffmpeg and ffprobe)
brew install ffmpeg

# Or download from https://evermeet.cx/ffmpeg/
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
# ffprobe is included in the ffmpeg package
```

**Windows:**
Download from https://ffmpeg.org/download.html#build-windows
# The Windows build includes both ffmpeg.exe and ffprobe.exe

## Installation

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the service:**
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

The service will be available at `http://localhost:8000`

## API Documentation

Once the service is running, you can access:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc

## API Endpoints

### Health Check
- `GET /health` - Check service health and FFmpeg/FFprobe availability

### Text to Audio
- `POST /api/v1/audio/text-to-audio` - Convert single text to audio

### CSV to Audio
- `POST /api/v1/audio/csv-to-audio` - Process CSV file with multiple language sentences

### File Management
- `GET /api/v1/audio/files` - List all generated audio files
- `GET /api/v1/audio/download/{filename}` - Download audio file
- `DELETE /api/v1/audio/files/{filename}` - Delete audio file

### Information
- `GET /api/v1/audio/supported-languages` - Get list of supported languages

## Usage Examples

### 1. Convert Single Text to Audio

```bash
curl -X POST "http://localhost:8000/api/v1/audio/text-to-audio" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Hello, how are you?",
    "language": "en",
    "output_filename": "hello.mp3"
  }'
```

### 2. Process CSV File

```bash
curl -X POST "http://localhost:8000/api/v1/audio/csv-to-audio" \
  -F "csv_file=@your_file.csv" \
  -F 'request={
    "languages": [
      {"column_index": 0, "language_code": "it", "flag": "🇮🇹"},
      {"column_index": 1, "language_code": "ru", "flag": "🇷🇺"}
    ],
    "output_filename": "lesson_1.mp3",
    "pause_duration": 5000,
    "silence_duration": 1000
  }'
```

### 3. Download Generated Audio

```bash
curl -O "http://localhost:8000/api/v1/audio/download/lesson_1.mp3"
```

### 4. Check Health

```bash
curl "http://localhost:8000/api/v1/audio/health"
```

**Expected response:**
```json
{
  "status": "healthy",
  "ffmpeg_available": true,
  "missing_tools": [],
  "supported_languages": {
    "it": "Italian",
    "ru": "Russian",
    "en": "English",
    ...
  }
}
```

**If FFmpeg or FFprobe is missing:**
```json
{
  "status": "unhealthy",
  "ffmpeg_available": false,
  "missing_tools": ["ffmpeg", "ffprobe"],
  "supported_languages": {...}
}
```
```

## CSV File Format

The CSV file should have columns corresponding to different languages. For example:

```csv
Ciao,Привет
Come stai?,Как дела?
Buongiorno,Доброе утро
```

## Supported Languages

- `it` - Italian 🇮🇹
- `ru` - Russian 🇷🇺
- `en` - English 🇺🇸
- `es` - Spanish 🇪🇸
- `fr` - French 🇫🇷
- `de` - German 🇩🇪
- `pt` - Portuguese 🇵🇹
- `ja` - Japanese 🇯🇵
- `ko` - Korean 🇰🇷
- `zh` - Chinese 🇨🇳

## Project Structure

```
backend/
├── main.py                 # FastAPI application entry point
├── requirements.txt        # Python dependencies
├── src/
│   ├── api/
│   │   └── audio.py       # API routes for audio endpoints
│   ├── core/
│   │   └── config.py      # Configuration settings
│   ├── models/
│   │   └── audio.py       # Pydantic models for requests/responses
│   └── services/
│       └── audio_service.py # Core audio processing logic
├── uploads/               # Temporary upload directory
└── outputs/              # Generated audio files
```

## Environment Variables

Create a `.env` file to customize settings:

```env
UPLOAD_DIR=uploads
OUTPUT_DIR=outputs
DEFAULT_PAUSE_DURATION=5000
DEFAULT_SILENCE_DURATION=1000
```

## Error Handling

The service includes comprehensive error handling for:
- Missing FFmpeg or FFprobe tools (with specific error messages)
- Invalid file formats
- Audio generation failures
- File not found errors
- Network connectivity issues

## Performance Considerations

- Large CSV files may take time to process
- Audio files are stored in the `outputs/` directory
- Consider implementing cleanup jobs for old files
- For production, consider using external storage (S3, etc.)

## Development

To run in development mode with auto-reload:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Docker Support

To run with Docker:

```dockerfile
FROM python:3.11-slim

# Install FFmpeg
RUN apt-get update && apt-get install -y ffmpeg

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## License

This project is part of the Repeatio application suite. 