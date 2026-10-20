"""USA Kids Channel - audio: Kokoro TTS voice + numpy music bed + mix."""
import os
import json
import wave
import numpy as np

BASE = os.path.dirname(os.path.abspath(__file__))
KOKORO_DIR = os.environ.get("KOKORO_DIR", os.path.join(os.path.dirname(BASE), "factory", "tts_kokoro"))
KOKORO_VOICE = os.environ.get("KIDS_VOICE", "af_heart")  # warm, clear female for kids
SR = 24000


def _kokoro():
    from kokoro_onnx import Kokoro
    kokoro = Kokoro(os.path.join(KOKORO_DIR, "kokoro-v1.0.fp16.onnx"),
                    os.path.join(KOKORO_DIR, "voices-v1.0.bin"))
    return kokoro


def tts_lines(texts, out_dir):
    """Synthesize each line to out_dir/line_XX.wav. Returns list of durations (s)."""
    os.makedirs(out_dir, exist_ok=True)
    kokoro = _kokoro()
    durs = []
    for i, txt in enumerate(texts):
        f = os.path.join(out_dir, f"line_{i:02d}.wav")
        audio, _sr = kokoro.create(txt + ".", voice=KOKORO_VOICE, speed=0.92, lang="en-us")
        audio = np.asarray(audio, dtype=np.float32)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        _write_wav(f, audio)
        durs.append(len(audio) / SR)
        print(f"tts: line {i} '{txt[:28]}' -> {durs[-1]:.2f}s", flush=True)
    return durs


def _write_wav(path, arr):
    arr = np.clip(arr, -1.0, 1.0)
    data = (arr * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(data.tobytes())


def _read_wav(path):
    with wave.open(path, "rb") as w:
        sr = w.getframerate()
        data = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16)
    return data.astype(np.float32) / 32768.0, sr


def _tone(freq, dur_s, sr=SR, amp=0.5, decay=6.0):
    """Marimba-like plucked tone: sine + 2nd harmonic with exponential decay."""
    n = int(dur_s * sr)
    t = np.arange(n) / sr
    env = np.exp(-decay * t) * (1 - np.exp(-90 * t))
    wave_ = (np.sin(2 * np.pi * freq * t)
             + 0.35 * np.sin(2 * np.pi * freq * 2 * t)
             + 0.15 * np.sin(2 * np.pi * freq * 3 * t))
    return amp * env * wave_


def music_bed(total_s, seed=1):
    """Cheerful I-V-vi-IV marimba loop at 110 BPM, childlike and bouncy."""
    rng = np.random.default_rng(seed)
    bpm = 110.0
    beat = 60.0 / bpm          # 0.545s
    chords = [
        [261.63, 329.63, 392.00],   # C major
        [392.00, 493.88, 587.33],   # G major
        [220.00, 261.63, 329.63],   # A minor
        [349.23, 440.00, 523.25],   # F major
    ]
    melody_pool = [523.25, 587.33, 659.25, 783.99, 880.00]
    out = np.zeros(int(total_s * SR) + SR, dtype=np.float32)
    t_beat = 0.0
    ci = 0
    while t_beat < total_s:
        ch = chords[ci % 4]
        # bass pluck on each beat
        bass = ch[0] / 2.0
        s = int(t_beat * SR)
        tone = _tone(bass, beat * 1.8, amp=0.30, decay=7.0)
        e = min(len(out), s + len(tone))
        out[s:e] += tone[:e - s]
        # chord pluck every second beat (offbeat bounce)
        if int(t_beat / beat) % 2 == 0:
            for f in ch[1:]:
                tone = _tone(f, beat * 1.4, amp=0.16, decay=8.0)
                e = min(len(out), s + len(tone))
                out[s:e] += tone[:e - s]
        # little sparkle melody note on some beats
        if rng.random() < 0.6:
            f = melody_pool[rng.integers(0, len(melody_pool))]
            tone = _tone(f, beat * 0.9, amp=0.12, decay=10.0)
            s2 = int((t_beat + beat / 2) * SR)
            e = min(len(out), s2 + len(tone))
            out[s2:e] += tone[:e - s]
        t_beat += beat
        ci += 1
    out = out[:int(total_s * SR)]
    out /= max(1.0, np.abs(out).max() / 0.9)
    return out * 0.22   # bed level under voice


def assemble(voice_wavs, starts, total_s, out_path):
    """Place voice lines at their start times over the music bed, soft-limit."""
    music = music_bed(total_s, seed=hash(os.path.basename(out_path)) % 100)
    mix = np.zeros(len(music), dtype=np.float32)
    mix[:len(music)] += music
    for f, st in zip(voice_wavs, starts):
        v, _sr = _read_wav(f)
        s = int(st * SR)
        e = min(len(mix), s + len(v))
        if e > s:
            mix[s:e] += v[:e - s] * 0.95
    # gentle normalization / soft clip
    peak = np.abs(mix).max()
    if peak > 0.95:
        mix *= 0.95 / peak
    mix = np.tanh(mix * 1.05)  # soft limiter, keeps child-safe smoothness
    pk = np.abs(mix).max()
    if 0 < pk < 0.85:
        mix *= 0.85 / pk          # healthy, clear loudness for little ears
    _write_wav(out_path, mix)
    print(f"audio: mixed {len(voice_wavs)} lines + music -> {out_path} "
          f"({total_s:.1f}s, peak {np.abs(mix).max():.2f})", flush=True)
    return out_path
