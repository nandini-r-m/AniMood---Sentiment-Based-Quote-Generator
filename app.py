from flask import Flask, render_template, request, redirect, url_for, session
import json
import re
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
app.secret_key = 'anime-secret-key-2024'

# Dummy users
USERS = {
    "admin": "secret",
    "demo": "demopw",
}

JSON_PATH = 'AnimeQuotes.json'

# Fallback quotes
FALLBACK = [
    {"Quote": "Believe in yourself and create your own destiny.", "Character": "Vegeta", "Anime": "Dragon Ball Z"},
    {"Quote": "Hard work is worthless for those that don't believe in themselves.", "Character": "Naruto", "Anime": "Naruto"},
    {"Quote": "I'll leave tomorrow's problems to tomorrow's me.", "Character": "Saitama", "Anime": "One Punch Man"},
    {"Quote": "Loneliness is the most terrible poverty.", "Character": "Rem", "Anime": "Re:Zero"},
    {"Quote": "Fear is not evil. It tells you what your weakness is.", "Character": "Gildarts", "Anime": "Fairy Tail"},
    {"Quote": "The world isn't perfect, but it's there for us doing the best it can.", "Character": "Roy Mustang", "Anime": "FMA"},
    {"Quote": "Sometimes I do feel like I'm a failure.", "Character": "Usagi", "Anime": "Sailor Moon"},
    {"Quote": "People's lives don't end when they die.", "Character": "Itachi", "Anime": "Naruto"},
]

# Load data
try:
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        quotes_data = json.load(f)
except:
    quotes_data = FALLBACK

analyzer = SentimentIntensityAnalyzer()

def preprocess(text):
    return re.sub(r'[^\w\s]', '', text.lower())

def classify_quote(q):
    score = analyzer.polarity_scores(preprocess(q))['compound']
    if score >= 0.05:
        return 'positive'
    elif score <= -0.05:
        return 'negative'
    return 'neutral'

# Add sentiment labels
for q in quotes_data:
    q['sentiment_class'] = classify_quote(q['Quote'])

def get_quotes(mood, n=3):
    filtered = [q for q in quotes_data if q['sentiment_class'] == mood]
    if not filtered:
        return []
    return random.sample(filtered, min(n, len(filtered)))

# Routes
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        u = request.form.get('username', '').strip()
        p = request.form.get('password', '')
        if USERS.get(u) == p:
            session['user'] = u
            return redirect(url_for('home'))
        error = "Invalid username or password."
    return render_template('login.html', error=error)

@app.route('/home', methods=['GET', 'POST'])
def home():
    if 'user' not in session:
        return redirect(url_for('login'))

    mood, quotes = None, []

    if request.method == 'POST':
        mood = request.form.get('mood')
        if mood in ('positive', 'neutral', 'negative'):
            quotes = get_quotes(mood)

    return render_template('index.html', user=session['user'], mood=mood, quotes=quotes)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

# Required for Vercel
app = app
