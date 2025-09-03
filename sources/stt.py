import speech_recognition as sr

def stt(language="fr-FR"):
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300    # ambient noise energy level
    recognizer.pause_threshold = 0.8     # seconds of silence before stopping

    with sr.Microphone() as source:
        print("🎙️ Speak now... (listening will stop when you pause)")
        recognizer.adjust_for_ambient_noise(source, duration=1)

        try:
            audio = recognizer.listen(source, timeout=None)  # waits until you speak
            print("⏹️ Finished listening, recognizing...")

            text = recognizer.recognize_google(audio, language=language)
            print("🗣️ Recognized text:", text)
            return text

        except sr.UnknownValueError:
            print("❌ Could not understand the audio")
        except sr.RequestError as e:
            print(f"⚠️ API error: {e}")

if __name__ == "__main__":
    stt(language="fr-FR")