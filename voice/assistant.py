import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import time

def listen_for_city():
    """
    Listens to the microphone and returns the spoken text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Adjusting for ambient noise...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            return True, text
        except sr.WaitTimeoutError:
            return False, "Listening timed out."
        except sr.UnknownValueError:
            return False, "Could not understand audio."
        except sr.RequestError as e:
            return False, f"Could not request results; {e}"
        except Exception as e:
            return False, str(e)

def speak_text(text):
    """
    Converts text to speech and plays it.
    """
    try:
        tts = gTTS(text=text, lang='en')
        filename = "temp_audio.mp3"
        tts.save(filename)
        
        # Initialize pygame mixer to play audio
        pygame.mixer.init()
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        
        # Wait for the audio to finish playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
            
        pygame.mixer.quit()
        # Clean up
        if os.path.exists(filename):
            os.remove(filename)
    except Exception as e:
        print(f"Error speaking text: {e}")

def extract_city_from_command(command):
    """
    Simple heuristic to extract city name from a command like 'Check Chennai AQI'.
    """
    command = command.lower()
    words = command.split()
    
    # Remove common filler words
    fillers = ['check', 'aqi', 'in', 'the', 'for', 'of', 'what', 'is', 'air', 'quality', 'pollution']
    city_words = [w for w in words if w not in fillers]
    
    if city_words:
        # Assume the remaining words are the city name
        return " ".join(city_words).title()
    return None
