import requests
import pygame
import os
from newspaper import Article

api_key = "sk_4a3d284fd19d91d63b4025bc29d149c97993ba481f7b06ba"
voice_ID = "pFZP5JQG7iQjIQuC4Bku"


def generate_swedish_speech(text, output_path, api_key):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_ID}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "text": text,
        "voice_settings": {
            "stability": 0.7,
            "similarity_boost": 0.8
        }
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
        print("✅ Ljudfil skapad.")
    else:
        print(f" Fel vid skapande av tal: {response.status_code}")
        print(response.text)


def play_audio(file_path):
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()
    print("▶️ Spelar upp...")
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def get_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

if __name__ == "__main__":
    
    alt = input("Tjena, vill du använd URL(1) eller kopierad text(2). Tryck 1 eller 2: ")

    
    if (alt == "1"):
        url = input("URL: ").strip()
        text = get_article_text(url)
    else :
        text = input("Kopierad text: ")

    print("Hämtar..")
    output_file = "artikel.mp3"
    generate_swedish_speech(text, output_file, api_key)
    if os.path.exists(output_file):
        play_audio(output_file)
    else:
        print(" Inget ljud att spela upp.")
