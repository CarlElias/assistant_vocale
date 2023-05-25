import openai
import requests

openai.api_key = "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"


def speech_to_text(audio_binary):
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = base_url+'/speech-to-text/api/v1/recognize'
    # parametre du language de la requet HTTP
    params = {
        'model': 'fr-FR_Multimedia',
    }
    # body de notre requete HTTP
    body = audio_binary
    # Send a HTTP Post request
    response = requests.post(api_url, params=params, data=audio_binary).json()
    # insertion de la reponse dans la variable text
    """
    Struture de la reponse 
    {
    "response": {
        "results": {
        "alternatives": {
            "transcript": "Recognised text from your speech"
        }
        }
    }
    }
    """
    text = 'null'
    while bool(response.get('results')):
        print('speech to text response:', response)
        text = response.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)
        return text    


def text_to_speech(text, voice=""):
    # Watson Text to Speech HTTP Api url
    base_url = '...'
    api_url = base_url + '/text-to-speech/api/v1/synthesize?output=output_text.wav'
    # ajout du parametre de la voix dans l'url si l'user a choisi une voix de preference 
    if voice != "" and voice != "default":
        api_url += "&voice=" + voice
    # en-tête de requette http
    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json',
    }
    # Set the body of our HTTP request
    json_data = {
        'text': text,
    }
    # envoi du POST HTTP requette au service Watson Text to Speech
    """
    structure de la reponse 
        {
      "response": {
            content: The Audio data for the processed text to speech
        }
      }
    }
    """
    response = requests.post(api_url, headers=headers, json=json_data)
    print('text to speech response:', response)
    return response.content


def openai_process_message(user_message):
    # message "prompt" pour OpenAI Api
    prompt = "\"Agit comme un assistant personnel. tu peux repondre aux questions, traduire des phrases, faire un resume, et donner des recommandations : " + user_message + "\""
    # Appel de l'OpenAI Api pour traitement du prompt
    openai_response = openai.Completion.create(model="text-davinci-003", prompt=prompt,max_tokens=4000)
    print("openai response:", openai_response)
    # pour obtenir le texte de la réponse correspondant a notre prompt
    """
    structure de la reponse 
        {
      "choices": [
          {"text": "The model's answer to our prompt"},
          ...,
          ...
        ]
    }
    """
    response_text = openai_response.choices[0].text
    return response_text
