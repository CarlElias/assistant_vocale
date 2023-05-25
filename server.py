import base64
import json
from flask import Flask, render_template, request
from worker import speech_to_text, text_to_speech, openai_process_message
from flask_cors import CORS
import os

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
"""
cors = CORS(app, resources={r"/*": {"origins": "*"}}) initialise l'extension CORS pour l'application Flask. 
Cela permet de définir les paramètres de partage des ressources entre différents domaines. Dans ce cas, la configuration indique que toutes les ressources (/*) peuvent être partagées depuis n'importe quelle origine (*), ce qui signifie que les requêtes CORS sont autorisées de n'importe quel domaine.
"""


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/speech-to-text', methods=['POST'])
def speech_to_text_route():
    print("processing speech to text")
    audio_binary = request.data # recupere l'user audio de la requette 
    text = speech_to_text(audio_binary) # appel de la fonction speech_to_text pour transcrire l'audio
    # Retour de la reponse à l'user au JSON format
    response = app.response_class(
        response=json.dumps({'text': text}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    print(response.data)
    return response


@app.route('/process-message', methods=['POST'])
def process_message_route():
    user_message = request.json['userMessage'] # recupere le message de l'utilisateur de la requette
    print('user_message', user_message)
    voice = request.json['voice'] # recupere la voix selctionné de l'utilisateur à partir de la requête
    print('voice', voice)
    # appel de la fonction openai_process_message pour traiter le message de l'user et recuperer la reponse retour
    openai_response_text = openai_process_message(user_message)
    # suppression des espaces vides
    openai_response_text = os.linesep.join([s for s in openai_response_text.splitlines() if s])
    # appel de la fonction text_to_speech pour convertir l' OpenAI Api reponse en audio
    openai_response_speech = text_to_speech(openai_response_text, voice)
    
    # convertir l'openai_response_speech en une chaîne de caractères Base64 afin de pouvoir l'envoyer dans la réponse JSON
    openai_response_speech = base64.b64encode(openai_response_speech).decode('utf-8')
    """
    Comme openai_response_speech est un type de données audio, 
    nous ne pouvons pas l'envoyer directement dans un JSON car il ne peut stocker que des données textuelles.
    Par conséquent, nous utiliserons quelque chose appelé « encodage base64 ». 
    En termes simples, nous pouvons convertir n'importe quel type de données binaires en une représentation textuelle en encodant les données au format base64. 
    Ainsi, nous utiliserons simplement base64.b64encode(openai_response_speech).decode('utf-8') et stockerons le résultat dans openai_response_speech.
    """
    
    # Envoie de la réponse JSON à l'user contenant la réponse du message à la fois sous forme de texte et d'audio
    response = app.response_class(
        response=json.dumps({"openaiResponseText": openai_response_text, "openaiResponseSpeech": openai_response_speech}),
        status=200,
        mimetype='application/json'
    )
    print(response)
    return response

if __name__ == '__main__':
    app.run()