from django.shortcuts import render
import re
import requests

from django.shortcuts import render
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from googletrans import Translator


from gtts import gTTS
import os
from django.conf import settings
from django.http import HttpResponse


def main (request):
    return render(request,'main.html')

# Create a function to generate the audio file for a word
def generate_audio(word):
    tts = gTTS(word, lang='en')  # Generate speech in English
    audio_path = os.path.join(settings.MEDIA_ROOT, f'{word}.mp3')
    tts.save(audio_path)  # Save audio file to media directory

    # Return the relative path to the audio file that will be accessible via the web
    return os.path.join(settings.MEDIA_URL, f'{word}.mp3')


from django.shortcuts import render
import re
import requests
from concurrent.futures import ThreadPoolExecutor
from googletrans import Translator
from gtts import gTTS
import os
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render
import re
from googletrans import Translator

translator = Translator()



# Initialize translator
translator = Translator()

# Define stopwords
STOPWORDS = {
    'is', 'am', 'are', 'the', 'a', 'an', 'this', 'that', 'your', 'what',
    'of', 'and', 'to', 'in', 'on', 'for', 'it', 'as', 'at', 'by', 'with'
}

def extract_keywords(paragraph):
    """Extract meaningful words from the paragraph."""
    words = re.findall(r'\b\w+\b', paragraph.lower())
    return sorted(
        {word for word in words if word not in STOPWORDS and len(word) > 1}
    )

def fetch_data_from_api(word):
    """Fetch word meaning, synonyms, and antonyms from Free Dictionary API."""
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            meanings = data[0].get("meanings", [])
            if meanings:
                definition = meanings[0]["definitions"][0].get("definition", "")
                synonyms = meanings[0].get("synonyms", [])
                antonyms = meanings[0].get("antonyms", [])
                return definition, synonyms[:3], antonyms[:3]  # Return top 3 synonyms/antonyms
        return "", [], []  # Return blanks if no data is found
    except Exception as e:
        print(f"Error fetching data for {word}: {e}")
        return "", [], []

def translate_to_bangla(word):
    """Translate a word to Bangla using Google Translator."""
    try:
        translated = translator.translate(word, src="en", dest="bn")
        return translated.text
    except Exception as e:
        return "Error translating"


def generate_audio(word):
    """Generate audio file for the given word."""
    try:
        tts = gTTS(word, lang='en')  # Generate speech in English
        audio_path = os.path.join(settings.MEDIA_ROOT, f'{word}.mp3')
        tts.save(audio_path)  # Save audio file to media directory
        print(f"Audio file saved at: {audio_path}")  # Debug log
        return f"{settings.MEDIA_URL}{word}.mp3"
    except Exception as e:
        print(f"Error generating audio for {word}: {e}")
        return ""
    


# Home view
def home(request):
    return render(request, 'home.html')


def kyeword(request):
    """Keyword view: Process input and fetch word data."""
    words_data = []
    if request.method == 'POST':
        paragraph = request.POST.get('paragraph', '')
        words = extract_keywords(paragraph)  # Extract keywords

        # Use ThreadPoolExecutor to parallelize API calls
        with ThreadPoolExecutor() as executor:
            api_results = executor.map(fetch_data_from_api, words)
            translations = executor.map(translate_to_bangla, words)

        # Combine results and generate audio
        for word, api_result, bangla_translation in zip(words, api_results, translations):
            definition, synonyms, antonyms = api_result
            audio_path = generate_audio(word)  # Generate audio for the word

            words_data.append({
                'word': word,
                'meaning': bangla_translation if bangla_translation else definition,
                'synonyms': ", ".join(synonyms) if synonyms else "--",
                'antonyms': ", ".join(antonyms) if antonyms else "--",
                'audio': audio_path  # Pass the audio path to the template
            })

    return render(request, 'kyeword.html', {'words_data': words_data})






from django.shortcuts import render
from googletrans import Translator
import re

translator = Translator()

# Stopwords list
STOPWORDS = {
    'is', 'am', 'are', 'the', 'a', 'an', 'this', 'that', 'your', 'what',
    'of', 'and', 'to', 'in', 'on', 'for', 'it', 'as', 'at', 'by', 'with'
}

def extract_keywords(paragraph):
    """Extract meaningful words from the paragraph."""
    words = re.findall(r'\b\w+\b', paragraph.lower())  # Tokenize words
    filtered_words = {
        word for word in words
        if word not in STOPWORDS and not word.isnumeric() and len(word) > 1
    }
    return list(filtered_words)  # Return as a list

def translate_to_bangla(word):
    """Translate a word to Bangla using Google Translator."""
    try:
        translated = translator.translate(word, src="en", dest="bn")
        return translated.text
    except Exception as e:
        return "Error translating"

# View for reading input
def readinginput(request):
    """Render input form for paragraph submission."""
    return render(request, 'readinginput.html')


def readingtranslator(request):
    """Render translated words."""
    paragraph = request.POST.get('paragraph', '')
    return render(request, 'readingtranslator.html', {'paragraph': paragraph})


def translate_word_ajax(request):
    """Handle AJAX request to translate a word."""
    if request.method == 'GET':
        word = request.GET.get('word', '')
        if word:
            translation = translate_to_bangla(word)
            return JsonResponse({'word': word, 'translation': translation})
        return JsonResponse({'error': 'Invalid word'}, status=400)

