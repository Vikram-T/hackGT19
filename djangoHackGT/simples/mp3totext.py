import pydub
from pydub import AudioSegment
import io
import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud.speech import types
import wave
from google.cloud import storage
import shutil
class mp3totext:
    def __init__(self, mp3_fileHandle):
        self.mp3_fileHandle = mp3_fileHandle
    #mp3 to wav
    def mp3_to_wav(self):
        #specify where the ffmpeg is located
        pydub.AudioSegment.converter = shutil.which("ffmpeg")
        sound = AudioSegment.from_mp3(self.mp3_fileHandle.name)
        self.wav_file_name = self.mp3_fileHandle.name.split('.')[0] + '.wav'
        #exporting audio
        sound.export(self.wav_file_name, format="wav")
        print("Converted {} to {}".format(self.mp3_fileHandle.name, self.wav_file_name))

    def frame_rate_channel(self):
        """Required for GCP API"""
        self.wave_file = wave.open(self.wav_file_name, "rb")
        self.frame_rate = self.wave_file.getframerate()
        self.channels = self.wave_file.getnchannels()

    def upload_blob(self, bucket_name):
        """Uploads source_file_name to the bucket as destination_blob_name."""
        if '/' in self.wav_file_name:
            self.uploadName = os.path.basename(self.wav_file_name)
        else:
            self.uploadName = self.wav_file_name
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(self.uploadName)

        blob.upload_from_filename(self.wav_file_name)

        print('File {} uploaded as {} to google cloud.'.format(
            self.wav_file_name,
            self.uploadName))

    def delete_blob(self, bucket_name):
        """Deletes audio_file_name from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(self.uploadName)
        blob.delete()

        print('Blob {} deleted.'.format(self.uploadName))

    def sample_long_running_recognize(self):
        """
            Transcribe long audio file from Cloud Storage using asynchronous speech
            recognition

            Args:
            storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
        """
        self.mp3_to_wav()
        self.frame_rate_channel() #Gives frame rate and channels, needed for gcp
        self.upload_blob("102619hackgtaudio")

        client = speech_v1.SpeechClient()

        # Encoding of audio data sent. This sample sets this explicitly.
        # This field is optional for FLAC and WAV audio formats.
        encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
        config = {
            "sample_rate_hertz": self.frame_rate,
            "language_code": "en-US",
            "encoding": encoding,
            "audio_channel_count" : self.channels,
            "enable_automatic_punctuation" : True,
        }
        storage_uri = "gs://102619hackgtaudio/" + self.uploadName
        audio = {"uri": storage_uri}

        operation = client.long_running_recognize(config, audio)
        print(u"Waiting for operation to complete...")
        response = operation.result()

        file = open(self.wav_file_name + "_transcript.txt", "w", encoding='utf-8')

        for result in response.results:
            # First alternative is the most probable result
            alternative = result.alternatives[0]
            file.write("{}".format(alternative.transcript))
        file.close()

        self.delete_blob("102619hackgtaudio")


# upload_blob("102619hackgtaudio","Transcript.txt","Transcript.txt")

if __name__ == "__main__":
    # for audio_file_name in os.listdir(filepath):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"../HackGT-77a8a0d36669.json"
    audio_file_name = open(r"../media/gcpTestAudio.mp3", 'r')
    lecture = mp3totext(audio_file_name)
    lecture.sample_long_running_recognize()

#mp3_to_wav("Interpreting_line_plots.mp3")
