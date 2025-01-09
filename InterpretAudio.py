import whisper

model = whisper.load_model('tiny.en')

def transcribeAudio(filename):
    result = model.transcribe(filename)
    return result['text']

def getWordFromSentence(sentence):
    onlyLetters = ""
    for chr in sentence:
        if chr.isalpha() or chr == " ":
            onlyLetters += chr
    listOfWords = onlyLetters.split(" ")
    return listOfWords[-1]

if __name__ == '__main__':
    print(transcribeAudio('word.wav'))
    print(getWordFromSentence(transcribeAudio('word.wav')))