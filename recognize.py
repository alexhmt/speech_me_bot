from argparse import ArgumentParser
import os
from speechkit import model_repository, configure_credentials, creds
from speechkit.stt import AudioProcessingType
from config import config
import os,sys
from pydub import AudioSegment
from pathlib import Path


# Authentication via an API key.
configure_credentials(
   yandex_credentials=creds.YandexCredentials(
      api_key=config["YANDEX_CLOUD"]["API_SECRET_KEY"]
   )
)

def convert_ogg_to_wav(input_file):
    # Read the OGG audio file
    
    wav_path = str(Path(input_file).parent) + "/" + Path(input_file).stem + ".wav"
    audio = AudioSegment.from_ogg(input_file)
    audio.export(wav_path, format="wav")
    return wav_path

def convert_mp4_to_wav(input_file):
    # Read the OGG audio file
    
    wav_path = str(Path(input_file).parent) + "/" + Path(input_file).stem + ".wav"
    audio = AudioSegment.from_file(input_file, format="mp4")
    audio.export(wav_path, format="wav")
    return wav_path


def recognize_audio(audio):
   model = model_repository.recognition_model()

   # Set the recognition settings.
   model.model = 'general'
   model.language = 'ru-RU'
   model.audio_processing_type = AudioProcessingType.Full

   # Recognition of speech in the specified audio file and output of results to the console.
   result = model.transcribe_file(audio)
   for c, res in enumerate(result):
      if res.normalized_text:
         return f"✍️\n{res.normalized_text}"
      return "🤷‍♂️"
      # if res.has_utterances():
      #    print('utterances:')
      #    for utterance in res.utterances:
      #       print(utterance)

      