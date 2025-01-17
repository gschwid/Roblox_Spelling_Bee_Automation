import pyaudiowpatch as pyaudio
import time
import wave
import pyautogui
import whisper

class AudioHandler:
    """
    A class to handle all the audio recording and transcribing for the Roblox Spelling Bee Bot.

    Attributes:
        CHUNK_SIZE: Chunk size of audio files.
        _model: An instance of the Whisper model.
        _p: instance of the PyAudio class.
        _defaultSpeakers: Information about the default loopback device.
    """

    CHUNK_SIZE = 512
    _model = whisper.load_model('tiny.en')
    _p = pyaudio.PyAudio()
    
    def __init__(self):
        self._defaultSpeakers = self.initialzeRecordingSetup()

    def initialzeRecordingSetup(self):
        """
        Initializes the information about the loopback device using the WASAPI.
        """
        wasapi_info = self._p.get_host_api_info_by_type(pyaudio.paWASAPI)
        try:
            default_speakers = self._p.get_device_info_by_index(wasapi_info["defaultOutputDevice"])
        except OSError:
                raise RuntimeError("WASAPI is not available. This code will not work.")
        if not default_speakers["isLoopbackDevice"]:
            for loopback in self._p.get_loopback_device_info_generator():
                if default_speakers["name"] in loopback["name"]:
                        default_speakers = loopback
                        return default_speakers
        else:
            raise RuntimeError("Default loopback device not found.")

    def create_callback(self, waveFile):
        """
        Creates the callback function used by PyAudio to record audio clips.

        Attributes:
            waveFile (str): name of wive file recorded too.
        """
        def callback(in_data, frame_count, time_info, status):
            waveFile.writeframes(in_data)
            return (in_data, pyaudio.paContinue)
        return callback

    def createAudioFile(self, filesCreated, filename, sleepFunction):
        """
        Creates an audio file.

        Attributes:
            filename (str): name of wive file recorded too.
            sleepFunction: function that determines how long the recording goes on for. 
        """
        wave_file = wave.open(filename, 'wb')
        wave_file.setnchannels(1)
        wave_file.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        wave_file.setframerate(int(self._defaultSpeakers["defaultSampleRate"]))
        callback = self.create_callback(wave_file)  
        with self._p.open(format=pyaudio.paInt16,
            channels=1,
            rate=int(self._defaultSpeakers["defaultSampleRate"]),
            frames_per_buffer=self.CHUNK_SIZE,
            input=True,
            input_device_index=self._defaultSpeakers["index"],
            stream_callback=callback
        ) as stream:             
            print(f'recording stream to {filename}, stopping when repeat button detected...')
            if sleepFunction(0.5, 7):
                wave_file.close()
                return True
            else:
                wave_file.close()
                return False

    def releaseAudioResources(self):
        """
        Frees all memory associated with PyAudio.
        """
        print("Ending audio...")
        self._p.terminate()
    
    def transcribeAudio(self, filename):
        """
        Transcribes text from an audio file.

        Attributes:
            filename (str): name of wive file being transcribed.
        """
        result = self._model.transcribe(filename)
        return result['text']

    def getWordFromSentence(self, sentence):
        """
        Extracts desired word to spell from sentence.

        Attributes:
            sentence (str): string with the transcribed spelling bee audio.
        """
        onlyLetters = ""
        for chr in sentence:
            if chr.isalpha() or chr == " ":
                onlyLetters += chr
        listOfWords = onlyLetters.split(" ")
        return listOfWords[-1]
