
import os
from google.cloud import language_v1
from google.cloud.language_v1 import enums
from google.cloud import storage
import json

class NLP_GCP:
    def __init__(self, fileName):
        self.fileName = fileName
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/Users/josh/hackGT19/djangoHackGT/HackGT-77a8a0d36669.json"


    def sample_analyze_entities(self, gcs_content_uri):
        """
        Analyzing Entities in text file stored in Cloud Storage
        Args:
          gcs_content_uri Google Cloud Storage URI where the file content is located.
          e.g. gs://[Your Bucket]/[Path to File]
        """

        client = language_v1.LanguageServiceClient()

        # gcs_content_uri = 'gs://cloud-samples-data/language/entity.txt'

        # Available types: PLAIN_TEXT, HTML
        type_ = enums.Document.Type.PLAIN_TEXT

        # Optional. If not specified, the language is automatically detected.
        # For list of supported languages:
        # https://cloud.google.com/natural-language/docs/languages
        language = "en"
        document = {"gcs_content_uri": gcs_content_uri, "type": type_, "language": language}

        # Available values: NONE, UTF8, UTF16, UTF32
        encoding_type = enums.EncodingType.UTF8

        response = client.analyze_entities(document, encoding_type=encoding_type)
        WORDS = []
        WIKI = []
        # Loop through entitites returned from the API
        for entity in response.entities:
            # print(u"Representative name for the entity: {}".format(entity.name))
            # Get entity type, e.g. PERSON, LOCATION, ADDRESS, NUMBER, et al
            # print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
            # Get the salience score associated with the entity in the [0, 1.0] range
            # print(u"Salience score: {}".format(entity.salience))
            # Loop over the metadata associated with entity. For many known entities,
            # the metadata is a Wikipedia URL (wikipedia_url) and Knowledge Graph MID (mid).
            # Some entity types may have additional metadata, e.g. ADDRESS entities
            # may have metadata for the address street_name, postal_code, et al.
            for metadata_name, metadata_value in entity.metadata.items():
                # print(u"{}: {}".format(metadata_name, metadata_value))
                if(metadata_name == "wikipedia_url"):
                    WORDS.append(entity.name)
                    WIKI.append(metadata_value)
                    # print("ERERERERERERER")

            # Loop over the mentions of this entity in the input document.
            # The API currently supports proper noun mentions.
            # for mention in entity.mentions:
            #     print(u"Mention text: {}".format(mention.text.content))
            #     # Get the mention type, e.g. PROPER for proper noun
            #     print(
            #         u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            #     )

        # for entity in response.entities:
        #     if(entity.  )

        # Get the language of the text, which will be the same as
        # the language specified in the request or, if not specified,
        # the automatically-detected language.
        # print(u"Language of the text: {}".format(response.language))
        # return (response.language)
        return WORDS, WIKI
    def upload_blob(self,bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        if '/' in self.wav_file_name:
            self.uploadName = os.path.basename(self.wav_file_name)
        else:
            self.uploadName = self.wav_file_name
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        print(blob)

        blob.upload_from_filename(source_file_name)

        print('File {} uploaded to {}.'.format(
            source_file_name,
            destination_blob_name))

    def delete_blob(self,bucket_name, blob_name):
        """Deletes a blob from the bucket."""
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)

        blob.delete()

        print('Blob {} deleted.'.format(blob_name))

    def nat_lang_analysis(self,text_content):
        self.upload_blob("102619hackgtaudio",text_content,text_content)

        storage_uri = "gs://102619hackgtaudio/" + text_content

        WORDS, WIKI = self.sample_analyze_entities(storage_uri)


        for i in WORDS:
            print(i)

        with open('data.txt', 'w') as outfile:
            json.dump(sample_analyze_entities(storage_uri), outfile)

        delete_blob("102619hackgtaudio", text_content)
        return WORDS, WIKI

if __name__ == "__main__":
    # for audio_file_name in os.listdir(filepath):
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"/Users/josh/hackGT19/djangoHackGT/HackGT-77a8a0d36669.json"
    text_content = fileName
    WORDS, WIKI = nat_lang_analysis(text_content)
