import numpy as np
import librosa
import librosa.display
from pydub import AudioSegment
import IPython.display as ipd
import matplotlib.pyplot as plt
import os
import imageio.v3 as imageio
from matplotlib.animation import FuncAnimation
import uuid

def load_audio(file_path: str) -> tuple[np.ndarray, int]:
    """
    Load audio file and convert to mono with normalized samples.
    
    Args:
        file_path (str): Path to the audio file.
    
    Returns:
        tuple: (audio samples, sample rate)
    
    Raises:
        FileNotFoundError: If the audio file does not exist.
        ValueError: If the file format is not supported.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Audio file not found: {file_path}")
    
    try:
        # Load audio file
        audio = AudioSegment.from_file(file_path)
        
        # Convert to mono if stereo
        if audio.channels == 2:
            audio = audio.set_channels(1)
        
        # Get audio samples and sample rate
        samples = np.array(audio.get_array_of_samples(), dtype=np.float32) / (2**15)
        sample_rate = audio.frame_rate
        
        return samples, sample_rate, audio
    except Exception as e:
        raise ValueError(f"Failed to load audio file: {str(e)}")

def resample_audio(samples: np.ndarray, orig_sr: int, target_sr: int = 22050) -> tuple[np.ndarray, int]:
    """
    Resample audio to the target sample rate if necessary.
    
    Args:
        samples (np.ndarray): Audio samples.
        orig_sr (int): Original sample rate.
        target_sr (int): Target sample rate (default: 22050 Hz).
    
    Returns:
        tuple: (resampled audio samples, target sample rate)
    """
    if orig_sr != target_sr:
        samples = librosa.resample(samples, orig_sr=orig_sr, target_sr=target_sr)
        return samples, target_sr
    return samples, orig_sr

def save_audio(samples: np.ndarray, sample_rate: int, output_path: str, original_audio: AudioSegment) -> None:
    """
    Save processed audio samples to a file with the same format as the original.
    
    Args:
        samples (np.ndarray): Processed audio samples.
        sample_rate (int): Sample rate of the audio.
        output_path (str): Path to save the audio file.
        original_audio (AudioSegment): Original audio object for format reference.
    """
    # Convert normalized samples back to int16
    samples_int16 = (samples * (2**15)).astype(np.int16)
    
    # Create new AudioSegment
    audio_segment = AudioSegment(
        samples_int16.tobytes(),
        frame_rate=sample_rate,
        sample_width=2,  # 16-bit audio
        channels=1       # Mono
    )
    
    # Export audio file
    audio_segment.export(output_path, format=original_audio.format)

def generate_waveform_gif(samples: np.ndarray, sample_rate: int, output_path: str, duration: float = 5.0) -> None:
    """
    Generate and save a waveform animation as a GIF.
    
    Args:
        samples (np.ndarray): Audio samples.
        sample_rate (int): Sample rate of the audio.
        output_path (str): Path to save the GIF file.
        duration (float): Duration of the GIF in seconds (default: 5.0).
    """
    # Prepare figure
    fig, ax = plt.subplots(figsize=(10, 4))
    time = np.linspace(0, len(samples) / sample_rate, len(samples))
    
    # Initialize plot
    line, = ax.plot([], [])
    ax.set_xlim(0, duration)
    ax.set_ylim(np.min(samples) * 1.1, np.max(samples) * 1.1)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Amplitude")
    ax.set_title("Audio Waveform Animation")
    
    # Animation parameters
    frames = 100
    frame_duration = duration / frames
    samples_per_frame = int(sample_rate * frame_duration)
    
    def update(frame):
        start_idx = frame * samples_per_frame
        end_idx = min((frame + 1) * samples_per_frame, len(samples))
        line.set_data(time[start_idx:end_idx], samples[start_idx:end_idx])
        return line,
    
    # Create animation
    anim = FuncAnimation(fig, update, frames=frames, interval=1000 * frame_duration, blit=True)
    
    # Save GIF
    anim.save(output_path, writer='imageio', fps=1/frame_duration)
    plt.close(fig)

def process_audio(file_path: str, target_sr: int = 22050) -> tuple[np.ndarray, int, AudioSegment]:
    """
    Process audio file: load, convert to mono, normalize, and resample.
    
    Args:
        file_path (str): Path to the audio file.
        target_sr (int): Target sample rate (default: 22050 Hz).
    
    Returns:
        tuple: (processed audio samples, sample rate, original audio object)
    """
    # Load audio
    samples, sample_rate, original_audio = load_audio(file_path)
    
    # Resample if necessary
    samples, sample_rate = resample_audio(samples, sample_rate, target_sr)
    
    return samples, sample_rate, original_audio

def get_output_filenames(input_path: str) -> tuple[str, str]:
    """
    Generate output filenames for audio and GIF based on input filename.
    
    Args:
        input_path (str): Path to the input audio file.
    
    Returns:
        tuple: (audio output path, GIF output path)
    """
    filename = os.path.splitext(os.path.basename(input_path))[0]
    audio_output = f"sample_data/v2_{filename}{os.path.splitext(input_path)[1]}"
    gif_output = f"sample_data/v2_{filename}.gif"
    return audio_output, gif_output

def main():
    """
    Main function to process, save, and display audio, and generate GIF.
    """
    # Define file path
    file_path = "sample_data/mmmm.mov"
    
    try:
        # Process audio
        samples, sample_rate, original_audio = process_audio(file_path)
        
        # Generate output filenames
        audio_output_path, gif_output_path = get_output_filenames(file_path)
        
        # Save processed audio
        save_audio(samples, sample_rate, audio_output_path, original_audio)
        
        # Generate and save waveform GIF
        generate_waveform_gif(samples, sample_rate, gif_output_path)
        
        # Print audio information
        print(f"Audio loaded successfully, sample rate: {sample_rate}, duration: {len(samples)/sample_rate:.2f} seconds")
        print(f"Processed audio saved to: {audio_output_path}")
        print(f"Waveform GIF saved to: {gif_output_path}")
        
        # Display audio
        display_audio(samples, sample_rate)
        
    except Exception as e:
        print(f"Error processing audio: {str(e)}")

def display_audio(samples: np.ndarray, sample_rate: int) -> None:
    """
    Display audio using IPython's Audio widget.
    
    Args:
        samples (np.ndarray): Audio samples.
        sample_rate (int): Sample rate of the audio.
    """
    ipd.display(ipd.Audio(samples, rate=sample_rate))

if __name__ == "__main__":
    main()
