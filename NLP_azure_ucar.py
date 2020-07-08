from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import pymongo

key = ''
endpoint = 'https://ucar.cognitiveservices.azure.com/'
def authenticate_client():
    ta_credential = AzureKeyCredential(key)
    text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint, credential=ta_credential)
    return text_analytics_client

client = authenticate_client()

mongoclient = pymongo.MongoClient("mongodb://localhost:27017/")
mongodb = mongoclient["ucar"]
clean_coll = mongodb['clean_db']
result_coll = mongodb['result_db']


def sentiment_analysis_example(client):
    for doc in clean_coll.find()[0:5]:
        del doc['_id']
        doc['id'] = '1'
        documents = [doc]
        response = client.analyze_sentiment(documents=documents)[0]
        del doc['id']
        doc['sentiment'] = response.sentiment
        doc['positive'] = response.confidence_scores.positive
        doc['neutral'] = response.confidence_scores.neutral
        doc['negative'] = response.confidence_scores.negative
        print("Document Sentiment: {}".format(response.sentiment))
        print("Overall scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f} \n".format(
            response.confidence_scores.positive,
            response.confidence_scores.neutral,
            response.confidence_scores.negative,
        ))
        result_coll.insert_one(doc)


sentiment_analysis_example(client)


