from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from enum import Enum

class LanguageCode(str, Enum):
    ITALIAN = "it"
    RUSSIAN = "ru"
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    PORTUGUESE = "pt"
    JAPANESE = "ja"
    KOREAN = "ko"
    CHINESE = "zh"

class LanguageConfig(BaseModel):
    column_index: int = Field(..., description="Column index in CSV")
    language_code: LanguageCode = Field(..., description="Language code")
    flag: str = Field(..., description="Flag emoji for the language")

class AudioGenerationRequest(BaseModel):
    languages: List[LanguageConfig] = Field(
        default=[
            LanguageConfig(column_index=0, language_code=LanguageCode.ITALIAN, flag="🇮🇹"),
            LanguageConfig(column_index=1, language_code=LanguageCode.RUSSIAN, flag="🇷🇺")
        ],
        description="Language configurations"
    )
    output_filename: str = Field(default="output.mp3", description="Output audio filename")
    pause_duration: int = Field(default=5000, description="Pause duration between languages (ms)")
    silence_duration: int = Field(default=1000, description="Silence duration between sentences (ms)")

class AudioGenerationResponse(BaseModel):
    success: bool
    message: str
    output_file: Optional[str] = None
    error: Optional[str] = None

class TextToAudioRequest(BaseModel):
    text: str = Field(..., description="Text to convert to audio")
    language: LanguageCode = Field(default=LanguageCode.ITALIAN, description="Language code")
    output_filename: Optional[str] = Field(None, description="Output filename")

class TextToAudioResponse(BaseModel):
    success: bool
    message: str
    audio_file: Optional[str] = None
    error: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    ffmpeg_available: bool
    missing_tools: List[str] = []
    supported_languages: Dict[str, str] 