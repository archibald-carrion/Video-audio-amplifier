# backend.py
import os
from dataclasses import dataclass
from typing import Optional, Callable
from moviepy.editor import VideoFileClip, AudioFileClip
from pydub import AudioSegment

@dataclass
class ProcessingStatus:
    is_processing: bool = False
    progress: float = 0.0
    status_message: str = ""
    error_message: Optional[str] = None

class VideoProcessor:
    def __init__(self):
        self._status = ProcessingStatus()
        self._status_callback: Optional[Callable[[ProcessingStatus], None]] = None
        
    def register_status_callback(self, callback: Callable[[ProcessingStatus], None]):
        self._status_callback = callback
        
    def _update_status(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self._status, key, value)
        if self._status_callback:
            self._status_callback(self._status)
    
    def amplify_audio(self, input_file: str, output_file: str, amplification_factor: float) -> bool:
        if self._status.is_processing:
            return False
            
        self._update_status(
            is_processing=True,
            progress=0.0,
            status_message="Starting processing...",
            error_message=None
        )
        
        temp_dir = "temp_audio_processing"
        os.makedirs(temp_dir, exist_ok=True)
        
        try:
            # Load video
            self._update_status(progress=10, status_message="Loading video file...")
            video = VideoFileClip(input_file)
            
            # Extract audio
            self._update_status(progress=20, status_message="Extracting audio...")
            audio = video.audio
            if audio is None:
                raise Exception("No audio found in input video")
            
            # Save temporary audio
            self._update_status(progress=30, status_message="Processing audio...")
            audio_file = os.path.join(temp_dir, "temp_audio.wav")
            audio.write_audiofile(audio_file)
            
            # Amplify audio
            self._update_status(progress=50, status_message="Amplifying audio...")
            audio_segment = AudioSegment.from_file(audio_file)
            amplified_audio_segment = audio_segment + (10 * amplification_factor)
            
            # Export amplified audio
            self._update_status(progress=70, status_message="Exporting amplified audio...")
            amplified_audio_file = os.path.join(temp_dir, "amplified_audio.wav")
            amplified_audio_segment.export(amplified_audio_file, format="wav")
            
            # Combine with video
            self._update_status(progress=80, status_message="Combining audio with video...")
            amplified_audio = AudioFileClip(amplified_audio_file)
            final_video = video.set_audio(amplified_audio)
            
            # Save final video
            self._update_status(progress=90, status_message="Saving final video...")
            final_video.write_videofile(output_file, audio_codec='aac')
            
            self._update_status(
                is_processing=False,
                progress=100,
                status_message="Processing complete!",
            )
            return True
            
        except Exception as e:
            self._update_status(
                is_processing=False,
                progress=0,
                status_message="Error occurred",
                error_message=str(e)
            )
            return False
            
        finally:
            # Cleanup
            if os.path.exists(temp_dir):
                for file in os.listdir(temp_dir):
                    try:
                        os.remove(os.path.join(temp_dir, file))
                    except:
                        pass
                os.rmdir(temp_dir)