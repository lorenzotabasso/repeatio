import os
import re
import tempfile
import subprocess
import pandas as pd
from gtts import gTTS
from pydub import AudioSegment
from typing import List, Tuple, Optional
from pathlib import Path

from src.core.config import settings
from src.models.audio import LanguageConfig


class AudioService:
    def __init__(self):
        self.supported_languages = settings.SUPPORTED_LANGUAGES
    
    def check_ffmpeg_tools(self) -> tuple[bool, list[str]]:
        """Check if ffmpeg and ffprobe are installed"""
        tools = ['ffmpeg', 'ffprobe']
        missing = []
        
        for tool in tools:
            try:
                subprocess.run([tool, '-version'], capture_output=True, check=True)
            except (FileNotFoundError, subprocess.CalledProcessError):
                missing.append(tool)
        
        if missing:
            print(f"❌ Error: The following tools are missing: {', '.join(missing)}")
            return False, missing
        return True, []
    
    def text_to_audio_segment(self, text: str, lang: str = 'it') -> AudioSegment:
        """Converts a string to an audio segment using gTTS"""
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
                tts = gTTS(text=text, lang=lang)
                tts.save(temp_file.name)
                audio = AudioSegment.from_mp3(temp_file.name)
                os.unlink(temp_file.name)
                return audio
        except Exception as e:
            raise Exception(f"Failed to convert text to audio: {str(e)}")
    
    def process_csv_to_audio(
        self,
        csv_file_path: str,
        output_audio: str,
        languages: List[LanguageConfig],
        pause_duration: int = 5000,
        silence_duration: int = 1000
    ) -> str:
        """
        Reads a CSV file, converts sentences to audio, and saves them in a single MP3 file with pauses.
        """
        try:
            # Read CSV file
            df = pd.read_csv(csv_file_path, header=None)
            
            # Rename columns based on language codes
            column_mapping = {lang.column_index: f'lang_{lang.language_code.value}' for lang in languages}
            df = df.rename(columns=column_mapping)
            
            # Data cleaning
            lang_columns = [f'lang_{lang.language_code.value}' for lang in languages]
            df = df.dropna(subset=lang_columns)
            
            for col in lang_columns:
                df = df[df[col].astype(str).str.strip() != '']
            df = df[~df[lang_columns[0]].astype(str).str.match(r'^\d+\.?\d*$')]
            
            # Audio segments
            final_audio = AudioSegment.silent(duration=1000)
            pause = AudioSegment.silent(duration=pause_duration)
            pause1sec = AudioSegment.silent(duration=silence_duration)
            
            print(f"Found {len(df)} valid sentences. Generating audio...")
            
            for index, row in df.iterrows():
                try:
                    sentences = []
                    for lang_config in languages:
                        sentence = str(row[f'lang_{lang_config.language_code.value}']).strip()
                        sentence = re.sub(r'[,.](?=\s)', '', sentence)
                        sentences.append(f"{lang_config.flag} {sentence}")
                    
                    print(" | ".join(sentences))
                    
                    # Generate audio for each language
                    for lang_config in languages:
                        sentence = str(row[f'lang_{lang_config.language_code.value}']).strip()
                        sentence = re.sub(r'[,.](?=\s)', '', sentence)
                        audio = self.text_to_audio_segment(sentence, lang=lang_config.language_code.value)
                        final_audio += audio
                        
                        if lang_config != languages[-1]:  # If not the last language
                            final_audio += pause
                        else:
                            final_audio += pause1sec
                            
                except Exception as e:
                    print(f"❌ Error in sentence {index + 1}: {e}")
                    continue
            
            # Save the final audio
            output_path = Path(settings.OUTPUT_DIR) / output_audio
            final_audio.export(str(output_path), format="mp3")
            print(f"✅ Audio saved as: {output_path}")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Failed to process CSV to audio: {str(e)}")
    
    def text_to_audio_file(
        self,
        text: str,
        language: str = 'it',
        output_filename: Optional[str] = None
    ) -> str:
        """
        Converts a single text to audio file
        """
        try:
            if not output_filename:
                output_filename = f"text_audio_{language}.mp3"
            
            output_path = Path(settings.OUTPUT_DIR) / output_filename
            
            # Generate audio
            audio_segment = self.text_to_audio_segment(text, lang=language)
            audio_segment.export(str(output_path), format="mp3")
            
            return str(output_path)
            
        except Exception as e:
            raise Exception(f"Failed to convert text to audio file: {str(e)}")
    
    def get_supported_languages(self) -> dict:
        """Get list of supported languages"""
        return self.supported_languages 