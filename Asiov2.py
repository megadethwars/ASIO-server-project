import sounddevice as sd
import subprocess
import ffmpeg
import numpy as np
import struct
import threading
# Obtener información sobre los dispositivos de entrada disponibles
input_devices = sd.query_devices()
rtsp_url = 'rtsp://127.0.0.1:5554/stream2'
print("Dispositivos de entrada disponibles:")
for i, device in enumerate(input_devices):
    print(i,device)

# Especificar el índice del dispositivo que deseas capturar
#input_device_index = int(input("Ingresa el número del dispositivo de entrada: "))

# Configuración de parámetros de audio
SAMPLE_RATE = 44100
CHANNELS = 2
device_input = 1
sd.default.device = 1
sd.default.latency = 'low'
sd.default.samplerate = 44100
sd.default.dtype = 'int16'
sd.default.blocksize = 1024



ffmpeg_command = [
    'ffmpeg',
    '-f', 's16le',
    '-ac', str(CHANNELS),
    '-ar', str(SAMPLE_RATE),
    '-i', '-',
    '-acodec', 'mp3',
    '-f', 'rtsp', rtsp_url
]
rtsp_url = "rtsp://127.0.0.1:5554/stream2"  # Cambiar por la URL del servidor RTSP
ffmpeg_process = None
stop_event = threading.Event()  # Evento para detener el proceso de streaming
def start_streaming_audio(sample_rate):
    process = (
        ffmpeg
        .input('pipe:', format='s16le', ac=2, ar=sample_rate)
        .output(
            rtsp_url,
            acodec="aac",
            preset="ultrafast",
            f="rtsp"
        )
        .overwrite_output()
        .run_async(pipe_stdin=True)
    )
    return process

def int16_to_little_endian_bytes(value):
    return struct.pack('<h', value)

def combine_and_convert_to_bytes(row):
    combined_value = row[1] * 255 + row[0]
    print(combined_value)
    if combined_value > 32767:
        combined_value -= 65536
    return struct.pack('<h', combined_value)

def audio_callback(indata, frames, time, status):
    global ffmpeg_process

    ffmpeg_process.stdin.write(indata.flatten().tobytes())




def run_audio_stream():
    global ffmpeg_process
    sample_rate = 44100  # Frecuencia de muestreo del audio
    #audio_stream = start_streaming_audio(sample_rate)
    ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE)
    with sd.InputStream(callback=audio_callback, channels=2, samplerate=sample_rate):
        while True:
            pass  # Pausa para permitir la escritura en la tubería

    audio_stream.stdin.close()
    audio_stream.wait()

if __name__ == "__main__":
    audio_thread = threading.Thread(target=run_audio_stream)
    audio_thread.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        stop_event.set()
        audio_thread.join()
