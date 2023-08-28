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

rtmp_url = "rtmp://localhost/live/STREAMTEST2"

ffmpeg_command_rtmp_image =  [
        'ffmpeg',
        '-loop', '1',
        '-i', 'C:/Users/leone/Music/Battletoads.jpg',  # Ruta de la imagen de fondo
        '-f',  's16le',             # Formato de audio WAV para FFmpeg
        '-ac', str(CHANNELS),              # Número de canales
        '-ar', str(SAMPLE_RATE),
        '-i', '-',           # Utilizamos una tubería para la entrada de audio
        '-c:a', 'aac',
        '-c:v', 'libx264',
        '-shortest',
        '-f', 'flv',
        rtmp_url
    ]

ffmpeg_command_rtsp = [
    'ffmpeg',
    '-f', 's16le',
    '-ac', str(CHANNELS),
    '-ar', str(SAMPLE_RATE),
    '-i', '-',
    '-acodec', 'mp3',
    '-f', 'rtsp', rtsp_url
]

ffmpeg_command_rtmp = [
    'ffmpeg',
    '-f', 's16le',
    '-ac', str(CHANNELS),
    '-ar', str(SAMPLE_RATE),
    '-i', '-',
    '-acodec', 'mp3',
    '-f', 'flv',  # Cambiar a formato FLV para RTMP
    rtmp_url  # URL del servidor RTMP
]

ffmpeg_command_hls = [
    'ffmpeg',
    '-f', 's16le',
    '-ac', str(CHANNELS),
    '-ar', str(SAMPLE_RATE),
    '-i', '-',
    '-acodec', 'aac',  # Cambiamos a AAC para HLS
    '-f', 'hls',      # Usamos el formato HLS
    '-hls_time', '10',  # Duración de los segmentos HLS en segundos
    '-hls_list_size', '6',  # Tamaño de la lista de reproducción HLS
    '-hls_segment_type', 'mpegts',  # Tipo de segmento HLS
    '-hls_flags', 'delete_segments',  # Eliminar segmentos antiguos
    'http://localhost:80/hls/STREAM_NAME.m3u8'  # Nombre de la lista de reproducción HLS
]

ffmpeg_command_http_flv = [
    'ffmpeg',
    '-f', 's16le',
    '-ac', str(CHANNELS),
    '-ar', str(SAMPLE_RATE),
    '-i', '-',
    '-acodec', 'aac',
    '-f', 'flv',  # Usamos el formato FLV
    'http://localhost:80/live/STREAM_NAME.flv'  # Aquí proporcionamos la URL HTTP-FLV como destino de salida
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


def audio_callback(indata, frames, time, status):
    global ffmpeg_process

    ffmpeg_process.stdin.write(indata.flatten().tobytes())




def run_audio_stream():
    global ffmpeg_process
    sample_rate = 44100  # Frecuencia de muestreo del audio
    
    ffmpeg_process = subprocess.Popen(ffmpeg_command_rtmp_image, stdin=subprocess.PIPE)
    #ffmpeg_process = subprocess.Popen(ffmpeg_command_rtmp, stdin=subprocess.PIPE)
    with sd.InputStream(callback=audio_callback, channels=2, samplerate=sample_rate):
        while True:
            pass  # Pausa para permitir la escritura en la tubería

    audio_stream.stdin.close()
    audio_stream.wait()

if __name__ == "__main__":
    audio_thread = threading.Thread(target=run_audio_stream)
    audio_thread.start()

    try:
        a=1
    except KeyboardInterrupt:
        stop_event.set()
        audio_thread.join()
