# import requests
# import pygame
# import os
# from newspaper import Article

# api_key = "sk_4a3d284fd19d91d63b4025bc29d149c97993ba481f7b06ba"
# voice_ID = "pFZP5JQG7iQjIQuC4Bku"


# def generate_swedish_speech(text, output_path, api_key):
#     url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_ID}"

#     headers = {
#         "xi-api-key": api_key,
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "text": text,
#         "voice_settings": {
#             "stability": 0.7,
#             "similarity_boost": 0.8
#         }
#     }

#     response = requests.post(url, headers=headers, json=payload)

#     if response.status_code == 200:
#         with open(output_path, "wb") as f:
#             f.write(response.content)
#         print("✅ Ljudfil skapad.")
#     else:
#         print(f" Fel vid skapande av tal: {response.status_code}")
#         print(response.text)


# def play_audio(file_path):
#     pygame.mixer.init()
#     pygame.mixer.music.load(file_path)
#     pygame.mixer.music.play()
#     print("▶️ Spelar upp...")
#     while pygame.mixer.music.get_busy():
#         pygame.time.Clock().tick(10)

# def get_article_text(url):
#     article = Article(url)
#     article.download()
#     article.parse()
#     return article.text

# if __name__ == "__main__":
    
#     alt = input("Tjena, vill du använd URL(1) eller kopierad text(2). Tryck 1 eller 2: ")

    
#     if (alt == "1"):
#         url = input("URL: ").strip()
#         text = get_article_text(url)
#     else :
#         text = input("Kopierad text: ")

#     print("Hämtar..")
#     output_file = "artikel.mp3"
#     generate_swedish_speech(text, output_file, api_key)
#     if os.path.exists(output_file):
#         play_audio(output_file)
#     else:
#         print(" Inget ljud att spela upp.")

import os
import requests
from flask import Flask, render_template, request, send_from_directory, send_file
from newspaper import Article

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'output'

api_key = "sk_45c97261b06a708053a2aa35991968a52c4408e4b659a793"
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
        return True
    else:
        print("❌ Fel från ElevenLabs:", response.status_code)
        return False

def get_article_text(url):
    article = Article(url)
    article.download()
    article.parse()
    return article.text

@app.route('/', methods=['GET', 'POST'])
def index():
    audio_file = None
    error = None

    if request.method == 'POST':
        choice = request.form.get('choice')
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], "artikel.mp3")

        try:
            if choice == 'url':
                url = request.form.get('url_input')
                text = get_article_text(url)
            else:
                text = request.form.get('text_input')

            success = generate_swedish_speech(text, output_path, api_key)

            print("klar med elevenlabs")
            print("skickar fil:", output_path)
            print("finns filen?", os.path.exists(output_path))
            if os.path.exists(output_path):
                print("filstorlek: ", os.path.getsize(output_path))
            print("pubilc URL: ", f"/output/{os.path.basename(output_path)}")

            if success:
                audio_file = 'artikel.mp3'
            else:
                error = "Kunde inte skapa ljudfil."
        except Exception as e:
            error = str(e)

    return render_template('index.html', audio_file=audio_file, error=error)

@app.route('/output/<filename>')
def serve_audio(filename):
    file_path = os.path.abspath(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    print("🔎 Absolut sökväg till filen:", file_path)

    if os.path.exists(file_path):
        print("✅ Filen finns.")
        return send_file(file_path, mimetype='audio/mpeg')
    else:
        print("❌ Filen hittades inte.")
        return "Fil hittades inte", 404



if __name__ == '__main__':
    os.makedirs('output', exist_ok=True)
    app.run(debug=True)
