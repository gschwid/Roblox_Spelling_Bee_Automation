import pyaudiowpatch as pyaudio
import time
import wave
import pyautogui
from DetectTurn import waitForPixelChange

# Code taken from..
# https://github.com/s0d3s/PyAudioWPatch/blob/master/examples/pawp_record_wasapi_loopback.py
# Has been slightly modified, look at the repository for more information on functionality.

DURATION = 3
CHUNK_SIZE = 512
#filename = "word.wav"
p = pyaudio.PyAudio()

wasapi_info = p.get_host_api_info_by_type(pyaudio.paWASAPI)
try:
    default_speakers = p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
except OSError:
        print("Looks like you dont have WASAPI... This code will not work")
        exit(1)
if not default_speakers["isLoopbackDevice"]:
    for loopback in p.get_loopback_device_info_generator():
        if default_speakers["name"] in loopback["name"]:
                default_speakers = loopback
                break
else:
    print("Default loop back device not found.")
    exit(1)

def create_callback(wave_file):
    def callback(in_data, frame_count, time_info, status):
        wave_file.writeframes(in_data)
        return (in_data, pyaudio.paContinue)
    return callback

def createAudioFile(filesCreated):
    #filename = 'Detected_Images/word' + str(filesCreated) + '.wav'
    filename = 'word.wav'
    wave_file = wave.open(filename, 'wb')
    wave_file.setnchannels(1)
    wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
    wave_file.setframerate(int(default_speakers["defaultSampleRate"]))
    callback = create_callback(wave_file)  
    with p.open(format=pyaudio.paInt16,
        channels=1,
        rate=int(default_speakers["defaultSampleRate"]),
        frames_per_buffer=CHUNK_SIZE,
        input=True,
        input_device_index=default_speakers["index"],
        stream_callback=callback
    ) as stream:             
        print(f'recording stream to {filename}, stopping when repeat button detected...')
        waitForPixelChange(1844,545, 0)
        wave_file.close()

def releaseAudioResources():
    print("Ending audio...")
    p.terminate()

if __name__ == '__main__':
    createAudioFile(2)
