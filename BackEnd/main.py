from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
import openai #(installer openai via pip install openai)
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set your OpenAI API key
openai.api_key = 'openai_api_key'

def analyze_text(text):
    tokens = nltk.word_tokenize(text.lower())
    tokens = [char for char in tokens if char not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if word not in stop_words]
    
    lemmatizer = WordNetLemmatizer()
    lemmatized_words = [lemmatizer.lemmatize(word) for word in tokens]

    return {"tokens": lemmatized_words, "response": "should be Tunisian recipe"}

class AnalyseTexteInput(BaseModel):
    texte: str

@app.post("/analyse")
def analyse_endpoint(analyse_input: AnalyseTexteInput):
    analyzed_data = analyze_text(analyse_input.texte)
    
    # Appelez OpenAI GPT-3.5-turbo pour générer une réponse
    response_from_gpt = generate_response_with_openai(analyzed_data)
    
    return {"analyzed_data": analyzed_data, "recette": response_from_gpt}

def generate_response_with_openai(analyzed_data):
    # Préparez une invite pour OpenAI GPT-3.5-turbo
    prompt = f"You are a helpful assistant. {analyzed_data['response']}. User: {analyzed_data['tokens']}"
    
    # Faire une demande à l'API OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003",  #Utilisez le moteur turbo GPT-3.5 approprié
        prompt=prompt,
        max_tokens=100,  # Ajustez le paramètre max_tokens si nécessaire
        temperature=0.7,  
        stop=None  # Vous pouvez ajouter des mots vides pour limiter la longueur de la réponse
    )
    
    return response.choices[0].text.strip()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)




