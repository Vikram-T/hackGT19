import pydub
from pydub import AudioSegment
import io
import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud.speech import types
import wave
from google.cloud import storage


#mp3 to wav
def mp3_to_wav(audio_file_name):
    #specify where the ffmpeg is located
    pydub.AudioSegment.converter = r"C:\Users\vivek\Anaconda3\envs\GCPVoiceRecognition\Library\bin\ffmpeg.exe"
    sound = AudioSegment.from_mp3(audio_file_name)
    audio_file_name_wav = audio_file_name.split('.')[0] + '.wav'
    #exporting audio
    sound.export(audio_file_name_wav, format="wav")
    return audio_file_name_wav
    

def frame_rate_channel(audio_file_name):
    file_name = audio_file_name
    print(file_name)
    wave_file = wave.open(file_name, "rb")
    frame_rate = wave_file.getframerate()
    channels = wave_file.getnchannels()
    return frame_rate,channels


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))

def delete_blob(bucket_name, blob_name):
    """Deletes a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)

    blob.delete()

    print('Blob {} deleted.'.format(blob_name))

def sample_long_running_recognize(audio_file_name):
    wav_file_name = mp3_to_wav(audio_file_name)
    frame_rate,channels = frame_rate_channel(wav_file_name)
    upload_blob("102619hackgtaudio",wav_file_name,wav_file_name)

    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = frame_rate

    #channels
    channel_count = channels

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
        "audio_channel_count" : channel_count,
        "enable_automatic_punctuation" : True,
    }

    storage_uri = "gs://102619hackgtaudio/" + wav_file_name

    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    file = open(wav_file_name + "_transcript.txt", "w")

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        file.write(u"{}".format(alternative.transcript))
    file.close()

    delete_blob("102619hackgtaudio", wav_file_name)


# upload_blob("102619hackgtaudio","Transcript.txt","Transcript.txt")

if __name__ == "__main__":
    # for audio_file_name in os.listdir(filepath):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:/Users/vivek/Dropbox (GaTech)/Projects/HackGT/HackGT-77a8a0d36669.json"
    audio_file_name = r"C:\Users\vivek\Dropbox (GaTech)\Projects\HackGT\Interpreting_line_plots.mp3"
    sample_long_running_recognize(audio_file_name)

#mp3_to_wav("Interpreting_line_plots.mp3")