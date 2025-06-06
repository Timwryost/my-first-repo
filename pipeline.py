import argparse
from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import soundfile as sf
from scipy.signal import stft
import mido


def load_audio(path: str) -> Tuple[np.ndarray, int]:
    """Load an audio file returning samples and sample rate."""
    samples, sample_rate = sf.read(path)
    if samples.ndim > 1:
        # Mix down to mono
        samples = np.mean(samples, axis=1)
    return samples, sample_rate


def compute_spectrogram(samples: np.ndarray, sample_rate: int, n_fft: int = 1024, hop_length: int = 512) -> np.ndarray:
    """Compute magnitude spectrogram using STFT."""
    f, t, Zxx = stft(samples, fs=sample_rate, nperseg=n_fft, noverlap=n_fft - hop_length)
    return np.abs(Zxx)


def physical_materialization(spectrogram: np.ndarray) -> np.ndarray:
    """Placeholder for the physical cymatic sculpture stage."""
    # In a real implementation this would control hardware. Here we simply return
    # the spectrogram as if it were a 3D shape representation.
    return spectrogram


def scan_surface(shape: np.ndarray) -> np.ndarray:
    """Placeholder for 3D scanning of the physical surface."""
    # Again, we just pass the data through.
    return shape


def extract_metrics(model: np.ndarray) -> Tuple[float, float, float]:
    """Extract simple metrics from the 3D model."""
    height = float(np.max(model))
    # Approximate complexity by mean absolute gradient
    complexity = float(np.mean(np.abs(np.diff(model))))
    # Simple dynamics metric: standard deviation
    dynamics = float(np.std(model))
    return height, complexity, dynamics


def map_to_musical(height: float, complexity: float, dynamics: float) -> Tuple[int, int, float, int]:
    """Map metrics to musical parameters."""
    pitch = int(np.clip(height * 127, 0, 127))
    velocity = int(np.clip(complexity * 127, 0, 127))
    duration = max(dynamics * 2, 0.1)  # seconds
    timbre = 0  # placeholder
    return pitch, velocity, duration, timbre


def to_midi(events: List[Tuple[int, int, float, int]], file_path: str) -> None:
    """Save events to a simple MIDI file."""
    mid = mido.MidiFile()
    track = mido.MidiTrack()
    mid.tracks.append(track)
    for pitch, velocity, duration, _ in events:
        track.append(mido.Message('note_on', note=pitch, velocity=velocity, time=0))
        ticks = int(duration * 480)
        track.append(mido.Message('note_off', note=pitch, velocity=0, time=ticks))
    mid.save(file_path)


def process(audio_path: str, midi_out: str) -> None:
    samples, sr = load_audio(audio_path)
    spec = compute_spectrogram(samples, sr)
    shape = physical_materialization(spec)
    model = scan_surface(shape)
    h, c, d = extract_metrics(model)
    events = [map_to_musical(h, c, d)]
    to_midi(events, midi_out)
    print(f"Saved MIDI to {midi_out}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Demo audio-to-shape pipeline")
    parser.add_argument("audio", help="Input audio file (wav)")
    parser.add_argument("midi", help="Output MIDI file")
    args = parser.parse_args()
    process(args.audio, args.midi)


if __name__ == "__main__":
    main()
