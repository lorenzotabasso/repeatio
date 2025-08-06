from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import FileResponse
from typing import List
import aiofiles
import os
from pathlib import Path

from src.models.audio import (
    AudioGenerationRequest,
    AudioGenerationResponse,
    TextToAudioRequest,
    TextToAudioResponse,
    HealthResponse
)
from src.services.audio_service import AudioService
from src.core.config import settings

router = APIRouter(prefix="/audio", tags=["audio"])

# Dependency to get audio service
def get_audio_service():
    return AudioService()

@router.get("/health", response_model=HealthResponse)
async def health_check(audio_service: AudioService = Depends(get_audio_service)):
    """Check the health of the audio service"""
    ffmpeg_available, missing_tools = audio_service.check_ffmpeg_tools()
    return HealthResponse(
        status="healthy" if ffmpeg_available else "unhealthy",
        ffmpeg_available=ffmpeg_available,
        missing_tools=missing_tools,
        supported_languages=audio_service.get_supported_languages()
    )

@router.post("/text-to-audio", response_model=TextToAudioResponse)
async def text_to_audio(
    request: TextToAudioRequest,
    audio_service: AudioService = Depends(get_audio_service)
):
    """Convert a single text to audio"""
    try:
        # Check if ffmpeg is available
        ffmpeg_available, missing_tools = audio_service.check_ffmpeg_tools()
        if not ffmpeg_available:
            missing_list = ", ".join(missing_tools)
            raise HTTPException(
                status_code=500,
                detail=f"FFmpeg tools are not available. Missing: {missing_list}. Please install ffmpeg and ffprobe."
            )
        
        # Generate audio file
        output_file = audio_service.text_to_audio_file(
            text=request.text,
            language=request.language.value,
            output_filename=request.output_filename
        )
        
        return TextToAudioResponse(
            success=True,
            message="Audio generated successfully",
            audio_file=output_file
        )
        
    except Exception as e:
        return TextToAudioResponse(
            success=False,
            message="Failed to generate audio",
            error=str(e)
        )

@router.post("/csv-to-audio", response_model=AudioGenerationResponse)
async def csv_to_audio(
    csv_file: UploadFile = File(...),
    request: AudioGenerationRequest = None,
    audio_service: AudioService = Depends(get_audio_service)
):
    """Convert CSV file with sentences to audio"""
    try:
        # Check if ffmpeg is available
        ffmpeg_available, missing_tools = audio_service.check_ffmpeg_tools()
        if not ffmpeg_available:
            missing_list = ", ".join(missing_tools)
            raise HTTPException(
                status_code=500,
                detail=f"FFmpeg tools are not available. Missing: {missing_list}. Please install ffmpeg and ffprobe."
            )
        
        # Validate file type
        if not csv_file.filename.endswith('.csv'):
            raise HTTPException(
                status_code=400,
                detail="Only CSV files are supported"
            )
        
        # Save uploaded file
        upload_path = Path(settings.UPLOAD_DIR) / csv_file.filename
        async with aiofiles.open(upload_path, 'wb') as f:
            content = await csv_file.read()
            await f.write(content)
        
        # Use default request if none provided
        if request is None:
            request = AudioGenerationRequest()
        
        # Process CSV to audio
        output_file = audio_service.process_csv_to_audio(
            csv_file_path=str(upload_path),
            output_audio=request.output_filename,
            languages=request.languages,
            pause_duration=request.pause_duration,
            silence_duration=request.silence_duration
        )
        
        # Clean up uploaded file
        os.remove(upload_path)
        
        return AudioGenerationResponse(
            success=True,
            message="Audio generated successfully from CSV",
            output_file=output_file
        )
        
    except Exception as e:
        return AudioGenerationResponse(
            success=False,
            message="Failed to generate audio from CSV",
            error=str(e)
        )

@router.get("/download/{filename}")
async def download_audio(filename: str):
    """Download generated audio file"""
    file_path = Path(settings.OUTPUT_DIR) / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Audio file not found"
        )
    
    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="audio/mpeg"
    )

@router.get("/supported-languages")
async def get_supported_languages(audio_service: AudioService = Depends(get_audio_service)):
    """Get list of supported languages"""
    return {
        "languages": audio_service.get_supported_languages(),
        "total": len(audio_service.get_supported_languages())
    }

@router.delete("/files/{filename}")
async def delete_audio_file(filename: str):
    """Delete a generated audio file"""
    file_path = Path(settings.OUTPUT_DIR) / filename
    
    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail="Audio file not found"
        )
    
    try:
        os.remove(file_path)
        return {"message": f"File {filename} deleted successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete file: {str(e)}"
        )

@router.get("/files")
async def list_audio_files():
    """List all generated audio files"""
    output_dir = Path(settings.OUTPUT_DIR)
    files = []
    
    if output_dir.exists():
        for file_path in output_dir.glob("*.mp3"):
            files.append({
                "filename": file_path.name,
                "size": file_path.stat().st_size,
                "created": file_path.stat().st_ctime
            })
    
    return {
        "files": files,
        "total": len(files)
    } 