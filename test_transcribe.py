import pyaudio
import wave

# --- Recording Parameters ---
frame_per_buffer1 = 3200
formate1 = pyaudio.paInt16  # 16-bit audio
channels1 = 1
rate = 16000
sec = 5
output_filename = "output.wav"

# --- Initialize PyAudio ---
p = pyaudio.PyAudio()

stream = p.open(
    format=formate1,
    channels=channels1,
    rate=rate,
    input=True,
    frames_per_buffer=frame_per_buffer1
)

print("start recording")

frames = []
# Calculate the number of chunks to read
for i in range(0, int(rate / frame_per_buffer1 * sec)):
    data = stream.read(frame_per_buffer1)
    frames.append(data)

# --- Stop Recording ---
stream.stop_stream()
stream.close()
p.terminate()

print("end recording")

# --- Save the recorded data as a WAV file ---
wf = wave.open(output_filename, 'wb')
wf.setnchannels(channels1)
# ⭐️ FIX: Set the sample width from the PyAudio format
wf.setsampwidth(p.get_sample_size(formate1))
# ⭐️ FIX: Set the frame rate
wf.setframerate(rate)
# ⭐️ FIX: Write the frames to the file
wf.writeframes(b''.join(frames))
# ⭐️ FIX: Close the file
wf.close()

print(f"File saved: {output_filename}")


import os
ffmpeg_path = r"c:\Users\tejas\Desktop\ml\project\New folder\speech_recognition\ffmpeg-8.0-essentials_build\ffmpeg-8.0-essentials_build\bin"
os.environ['PATH'] += ';' + ffmpeg_path

import warnings
import whisper

warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

model = whisper.load_model("base")

audio_file = os.path.join(os.path.dirname(__file__), "output.wav")
result = model.transcribe(audio_file)

print(result["text"])



import pyttsx3
engine = pyttsx3.init()
engine.say(result["text"])
engine.runAndWait()
