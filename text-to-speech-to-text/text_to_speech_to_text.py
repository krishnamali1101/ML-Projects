#!/usr/bin/env python
# coding: utf-8

# # Text to speech

# In[113]:


get_ipython().system('pip install gTTS ')
#Google Text-to-Speech


# In[114]:


get_ipython().system('brew install mpg123 # for mac')


# In[115]:


get_ipython().system('pip install mpyg321 # for win')


# In[116]:



def text_to_speech(mytext, out_file_path = 'demo.mp3'):
    #print(mytext)
    # Import the required module for text 
    # to speech conversion 
    from gtts import gTTS 
    import os 

    # Language in which you want to convert 
    language = 'en'

    # Passing the text and language to the engine, 
    # here we have marked slow=False. Which tells 
    # the module that the converted audio should 
    # have a high speed 
    myobj = gTTS(text=mytext, lang=language, slow=False) 

    # Saving the converted audio in a mp3 file named 
    # welcome 
    myobj.save(out_file_path) 

    # Playing the converted file 
    os.system("mpg123 " + out_file_path)


# In[117]:


text_to_speech("hello, my name is krishna")


# ---

# # speech to text

# In[118]:


get_ipython().system('pip install SpeechRecognition pyaudio')


# In[119]:


import speech_recognition as sr

r = sr.Recognizer()
m = sr.Microphone()


# In[121]:


harvard = sr.AudioFile('harvard.wav')
with harvard as source:
        audio = r.record(source)


# In[104]:


type(audio)


# In[105]:


r.recognize_google(audio)


# In[12]:


with harvard as source:
    audio1 = r.record(source, duration=4)
    audio2 = r.record(source, duration=10)
    
print(r.recognize_google(audio1))

r.recognize_google(audio2)


# In[106]:


# recognize_bing(): Microsoft Bing Speech
# recognize_google(): Google Web Speech API
# recognize_google_cloud(): Google Cloud Speech - requires installation of the google-cloud-speech package
# recognize_houndify(): Houndify by SoundHound
# recognize_ibm(): IBM Speech to Text
# recognize_sphinx(): CMU Sphinx - requires installing PocketSphinx
# recognize_wit(): Wit.ai


# ## recognize_speech_from_mic

# In[107]:


import random
import time

import speech_recognition as sr


def recognize_speech_from_mic(recognizer, microphone, language='en-US', full_responce=True):
    
    """Transcribe speech from recorded from `microphone`.
    List of supported languages can be found @ http://stackoverflow.com/a/14302134

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio, show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    if not full_responce:
        if response['transcription']:
            print(response["transcription"]["alternative"][0]["transcript"])
            return response["transcription"]["alternative"][0]["transcript"]
        else:
            return ''
        
    return response


# In[89]:


recognize_speech_from_mic(r, m,full_responce=True)


# In[90]:


recognize_speech_from_mic(r, m,full_responce=False)


# ---

# # Speech-to-text-to-Speech

# In[108]:


text_to_speech(recognize_speech_from_mic(r,m,full_responce=False))


# # Game

# In[112]:


if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = ["apple", "banana", "grape", "orange", "mango", "lemon"]
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

    # get a random word from the list
    word = random.choice(WORDS)

    # format the instructions string
    instructions = (
        "I'm thinking of one of these words:\n"
        "{words}\n"
        "You have {n} tries to guess which one.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    text_to_speech(instructions)
    time.sleep(1)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Speak!'.format(i+1))
            text_to_speech('Guess {}. Speak!'.format(i+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")
            text_to_speech("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        user_guess = guess["transcription"]["alternative"][0]["transcript"]
        
        # show the user the transcription
        print("You said: {}".format(user_guess))
        text_to_speech("You said: {}".format(user_guess))

        # determine if guess is correct and if any attempts remain
        guess_is_correct = user_guess.lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct! You win!".format(word))
            text_to_speech("Correct! You win!".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
            text_to_speech("Incorrect. Try again.\n")
        else:
            print("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            text_to_speech("Sorry, you lose!\nI was thinking of '{}'.".format(word))
            break


# # Ref

# https://realpython.com/python-speech-recognition/
#     
# https://github.com/realpython/python-speech-recognition
# 
# https://towardsdatascience.com/easy-text-to-speech-with-python-bfb34250036e

# In[ ]:




