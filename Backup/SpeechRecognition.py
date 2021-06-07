import speech_recognition as sr

class Recognizer():
    def __init__(self):
        # recognizer
        self.r = sr.Recognizer()
    
    def test_with_audio(self, audiofile):
        # capture data from a file
        audio_ = sr.AudioFile(audiofile)
        with audio_ as source:
            audio_data = self.r.record(source)
        #voice string
        voice_str = self.r.recognize_google(audio_data)
        return voice_str
    
    def read_from_microphone(self):
        mic = sr.Microphone() # change device_index if default is not available
        with mic as source:
            # for noise reduction
            # self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
        self.r.recognize_google(audio)
        return None

    def voice_str_parser(self, voice_str):
        return None