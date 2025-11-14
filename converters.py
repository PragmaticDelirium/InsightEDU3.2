from os import path
from pydub import AudioSegment

# files                                                                         
'''src = "transcript.mp3"
dst = "test.wav"'''
filemp3 = 'welcome1.mp3'
filewav = 'welcome.wav'

# convert wav to mp3                                                            
sound = AudioSegment.from_mp3(filemp3)
sound.export(filewav, format="wav")