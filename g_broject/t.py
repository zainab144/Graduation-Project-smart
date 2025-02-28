
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import googletrans
from googletrans import Translator
import pyaudio

# إنشاء مترجم
translator = Translator()

# إنشاء مُعَرِّف التعرف على الكلام
r = sr.Recognizer()

# استخدام الميكروفون كمصدر للصوت
with sr.Microphone() as source:
    print("Speak now...")
    # التقاط الصوت من الميكروفون
    audio = r.listen(source)
try:
    # تحويل الصوت إلى نص باللغة العربية
    text = r.recognize_google(audio, language='ar-AR')
    print(f"Original Text (Arabic): {text}")
    
    # ترجمة النص إلى اللغة الإنجليزية
    translation = translator.translate(text, dest='en')
    translated_text = translation.text  # حفظ النص المترجم
    print(f"Translated Text (English): {translated_text}")
    
    # تحويل النص المترجم إلى كلام بصوت عالٍ
    tts = gTTS(translated_text, lang='en', slow=False)
    tts.save("output.mp3")  # حفظ الملف الصوتي
    
    # تشغيل الملف الصوتي باستخدام playsound
    playsound("output.mp3")
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand the audio.")
except sr.RequestError as e:
    print(f"Could not request results from Google Speech Recognition service; {e}")
except Exception as ex:
    print(f"An error occurred: {ex}") 