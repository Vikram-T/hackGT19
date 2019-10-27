import requests
import os
import pprint
import re


class AzureKeyWords:
    """Used to extract keywords from a text file"""
    def __init__(self, fileName):
        """ Reads text, and splits based on sentences"""
        self.fileName = fileName
        textToAnalyze = open(self.fileName, "r")
        fullText = textToAnalyze.read()
        fullText = fullText.strip()
        self.sentences = re.split("\.|\?|\!", fullText)

    def splitAndSend(self, apiUrl, apiKey):
        """ Split text into <5000 character sections keeping sentences and send to Azure"""
        allPackets = []
        packet = ""
        for i in self.sentences:
            if (len(packet+i) <= 5000):
                packet += i + " "
            else:
                packet = packet[:-1]
                allPackets.append(packet)
                packet = ""
        # Creates and sends jsonData to Azure text analytics api
        documents = []
        for i in range(0, len(allPackets)):
            jsonPacket = {
                "language":"en",
                "id": str(i+1),
                "text": allPackets[i]
                }
            documents.append(jsonPacket)
        analyzePacket =  {
        "documents": documents
        }
        headers = {
            "Content-Type": "application/json",
            "Ocp-Apim-Subscription-Key": apiKey
        }
        self.r = requests.post(url=apiUrl, headers=headers, json=analyzePacket)
        return self.r
if __name__ == "__main__":
    url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.1/keyPhrases"
    MyInstance = AzureKeyWords("/Users/vikram/Documents/Programming/hackGT19/djangoHackGT/media/algo.txt")
    r = MyInstance.splitAndSend(url, "af38334380c747b0873a35753787def2");
    #Verifies if request succeded
    print(r.status_code)
    print(r.json()['documents'][0]['keyPhrases'])
    pp = pprint.PrettyPrinter(indent=4)
