import speech_recognition as sr
from nltk.tokenize import word_tokenize

class Recognizer():
    def __init__(self):
        # recognizer
        self.r = sr.Recognizer()
        self.word_dict = {'1':'one', '2':'two', '3':'three', '4':'four', '5':'five', '6':'six', '7':'seven', '8':'eight', '9':'nine'}
        self.alt_dict = {'for':'four', 'to':'two', 'too': 'two', 'once':'one', 'take':'steak'}
    
    def test_with_audio(self, audiofile):
        # capture data from a file
        audio_ = sr.AudioFile(audiofile)
        with audio_ as source:
            audio_data = self.r.record(source)
        #voice string
        voice_str = self.r.recognize_google(audio_data)
        return voice_str
    
    def read_from_microphone(self):
        # Setup the microphone
        mic = sr.Microphone() # change device_index if default is not available
        with mic as source:
            # for noise reduction
            self.r.adjust_for_ambient_noise(source)
            audio = self.r.listen(source)
        text = self.r.recognize_google(audio)
        print(text)

        return text

    def voice_str_parser(self, text):
        words = word_tokenize(text)
        print(words)

        for i in range(len(words)):
            if words[i] in self.word_dict:
                words[i] = self.word_dict[words[i]]
            if words[i] in self.alt_dict:
                words[i] = self.alt_dict[words[i]]
        print(words)

        return words