import assemblyai as aai
from elevenlabs import generate, stream
import openai
from dotenv import load_dotenv
import os
from langdetect import detect ,  LangDetectException

class AI_Ass:
    def __init__(self):
        load_dotenv()
        aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.elevenlabes_api_key = os.getenv("ELEVENLABS_API_KEY")
        self.full_transcript = [
            {"role": "system", "content": "You are a smart glasses assistant designed for personal use. Your features include object detection, face detection, voice detection, and natural language processing (NLP). Respond in both Arabic and English based on the language used by the user."}
        ]

    def start_transcription(self):
        self.transcriber = aai.RealtimeTranscriber(
            sample_rate=16000,
            on_data=self.on_data,
            on_open=self.on_open,
            on_error=self.on_error,
            on_close=self.on_close,
            end_utterance_silence_threshold=1000
        )
        self.transcriber.connect()
        microphone_stream = aai.extras.MicrophoneStream(sample_rate=16000) 
        self.transcriber.stream(microphone_stream)

    def stop_transcription(self):
        if self.transcriber:
            self.transcriber.close()
            self.transcriber = None

    def on_open(self, session_opened: aai.RealtimeSessionOpened):
        return

    def on_data(self, transcript: aai.RealtimeTranscript):
        if not transcript.text:
            return

        if isinstance(transcript, aai.RealtimeFinalTranscript):
            self.generate_ai_response(transcript)
        else:
            print(transcript.text, end="\r")

    def on_error(self, error: aai.RealtimeError):
        return

    def on_close(self):
        return

    def generate_ai_response(self, transcript):
        self.stop_transcription()

        self.full_transcript.append({"role": "user", "content": transcript.text})
        print(f"\npatient: {transcript.text}", end="\r\n")

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=self.full_transcript
        )

        ai_response = response.choices[0].message.content

        self.generate_audio(ai_response)

        self.start_transcription()

    def generate_audio(self, text):
        self.full_transcript.append({"role": "assistant", "content": text})
        print(f"\nAI Receptionist: {text}")

        audio_stream = generate(
            api_key=self.elevenlabes_api_key,
            text=text,
            voice="Rachel",  # في أصوات تانية كتير
            stream=True
        )
        stream(audio_stream)

    def detect_language(self, text):
        try:
            language = detect(text)
            return language
        except  LangDetectException:
            return "unknown"


if __name__ == "__main__":
    ai_assistant = AI_Ass()
    ai_assistant.start_transcription()



