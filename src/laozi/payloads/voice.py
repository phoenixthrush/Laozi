import pyttsx3

"""
engine = pyttsx3.init()
voices = engine.getProperty('voices')

for voice in voices:
    engine.setProperty('voice', voice.id)
    engine.say('Here we go round the mulberry bush.')

engine.runAndWait()
"""


def play_voice(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
