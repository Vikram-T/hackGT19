import os
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
from google.cloud import storage

def sample_long_running_recognize(storage_uri):
    """
    Transcribe long audio file from Cloud Storage using asynchronous speech
    recognition

    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """

    client = speech_v1.SpeechClient()

    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 48000

    # The language of the supplied audio
    language_code = "en-US"

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.LINEAR16
    config = {
        "sample_rate_hertz": sample_rate_hertz,
        "language_code": language_code,
        "encoding": encoding,
        "audio_channel_count" : 2,
        "enable_automatic_punctuation" : True,
    }
    audio = {"uri": storage_uri}

    operation = client.long_running_recognize(config, audio)

    print(u"Waiting for operation to complete...")
    response = operation.result()

    file = open("Transcript.txt", "w")

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        file.write(u"{}".format(alternative.transcript))
    file.close()
#storage_client = storage.Client.from_service_account_json('HackGT-77a8a0d36669.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:/Users/vivek/Dropbox (GaTech)/Projects/HackGT/HackGT-77a8a0d36669.json"

bucket_url = ("gs://102619hackgtaudio/longLecture.wav")
sample_long_running_recognize(bucket_url)

'''
def main():
    import argparse
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"C:/Users/vivek/Dropbox (GaTech)/Projects/HackGT/HackGT-77a8a0d36669.json"

    bucket_url = ("gs://102619hackgtaudio/Interpreting%20line%20plots.wav")
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--storage_uri",
        type=str,
        default=bucket_url,
    )
    args = parser.parse_args()

    sample_long_running_recognize(args.storage_uri)


if __name__ == "__main__":
    main()
'''