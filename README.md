Creation d'un assistant vocal 

## Contexte
Creation d'un assistant vocal en utilisant la technologie avancée de traitement du langage d'OpenAI et l'IA intégrable d'IBM Watson. 
l'assistant sera capable de comprendre et de répondre à des questions et demandes en temps réel, en utilisant la voix grâce aux capacités de conversion texte-parole et parole-texte

## requirement

- html
- css
- JavaScript
- python 3.8
- Flask-Cors
- flask
- ibm_watson

### A propose de Flask

Nous utilisereons Flask pour créer des routes et gérer les requêtes et réponses HTTP. 
Lorsqu'un utilisateur interagit avec l'assistant vocal via l'interface frontale, la requête sera envoyée au backend Flask. 
Flask traitera ensuite la requête et l'enverra au service approprié.

### Concernant docker (commande)
-docker build . -t assistant_vocale #aller a la ligne 
-docker run -p 8000:8000 assistant_vocale

### commande git 
git add .
git commit -m "message"
git push -u

