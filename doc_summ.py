# -*- coding: utf-8 -*-
"""
Created on Mon Jan 29 13:17:00 2024

@author: Tumisang.Lemao
"""
# Dependencies and Libraries
from flask import Flask, render_template, request, jsonify
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson.natural_language_understanding_v1 import Features, ConceptsOptions, EntitiesOptions, KeywordsOptions


app = Flask(__name__)

#IBM Watson NLU credentials
NLU_API_KEY = "7HLQaMFq7Vn2paLaR37OuU-Zgpa1nDn1iHnOJxsr_x-M"
NLU_URL = "https://api.au-syd.natural-language-understanding.watson.cloud.ibm.com/instances/ff06c55b-feb3-4a4d-b9c1-52e3a9f468ae"

#IBM Watson Assistant credentials
ASSISTANT_API_KEY ='lIxhQ9ulBND7X5gE1p-77MMy4uVDISN7pFieu-Qp3e_W'
ASSISTANT_URL = 'https://api.au-syd.assistant.watson.cloud.ibm.com/instances/5bac4a93-714a-40f9-91d6-212f7cbb6b73'


#Configure IBM Watson Natural Language Understanding service
authenticator = IAMAuthenticator(NLU_API_KEY)
nlu = NaturalLanguageUnderstandingV1(version='2019-07-12', authenticator=authenticator)
nlu.set_service_url(NLU_URL)

#Configure IBM Watson Assistant service
authenticator = IAMAuthenticator(ASSISTANT_API_KEY)
assistant = AssistantV2(
    version='2020-04-01',
    authenticator=authenticator
)
 
assistant.set_service_url(ASSISTANT_URL)

#Access the html
@app.route('/')
def index():
    return render_template('IBM_DEMO.html')

#Access the summarizer
@app.route('/summarize', methods=['POST'])
def summarize():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    

    text = file.read().decode('utf-8')
    

    response = nlu.analyze(text=text,
                           features=Features(entities=EntitiesOptions(),
                                             keywords=KeywordsOptions())).get_result()
    
    summary = response.get('usage', '')
    entities = response.get('keywords', [])
    
    return render_template('result.html', summary=summary, entities=entities)

#Access the chatbot
@app.route('/message', methods=['POST'])
def sendMessage():
    message = request.json['message']
    response = assistant.message_stateless(
        assistant_id='your-assistant-id',
        input={
            'message_type': 'text',
            'text': message
        }
    ).get_result()
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)


!python doc_summ.py
