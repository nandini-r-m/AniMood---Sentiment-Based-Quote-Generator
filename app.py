from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
import re
import json
import os
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
app.secret_key = 'anime-secret-key-2024'

USERS = {
    "admin": "password",
    "demo": "demo",
}

JSON_PATH = 'AnimeQuotes.json'

FALLBACK = [
    {"Quote": "Believe in yourself and create your own destiny.", "Character": "Vegeta", "Anime": "Dragon Ball Z"},
    {"Quote": "Hard work is worthless for those that don't believe in themselves.", "Character": "Naruto", "Anime": "Naruto"},
    {"Quote": "I'll leave tomorrow's problems to tomorrow's me.", "Character": "Saitama", "Anime": "One Punch Man"},
    {"Quote": "Loneliness is the most terrible poverty.", "Character": "Rem", "Anime": "Re:Zero"},
    {"Quote": "Fear is not evil. It tells you what your weakness is.", "Character": "Gildarts", "Anime": "Fairy Tail"},
    {"Quote": "The world isn't perfect, but it's there for us doing the best it can.", "Character": "Roy Mustang", "Anime": "FMA"},
    {"Quote": "Sometimes I do feel like I'm a failure. Like there's no hope for me.", "Character": "Usagi", "Anime": "Sailor Moon"},
    {"Quote": "People's lives don't end when they die. It ends when they lose faith.", "Character": "Itachi", "Anime": "Naruto"},
]

try:
    with open(JSON_PATH, 'r', encoding='utf-8') as f:
        df = pd.DataFrame(json.load(f))
except Exception:
    df = pd.DataFrame(FALLBACK)

analyzer = SentimentIntensityAnalyzer()

def preprocess(text):
    return re.sub(r'[^\w\s]', '', text.lower())

df['compound'] = df['Quote'].apply(lambda q: analyzer.polarity_scores(preprocess(q))['compound'])
df['sentiment_class'] = df['compound'].apply(
    lambda c: 'positive' if c >= 0.05 else ('negative' if c <= -0.05 else 'neutral')
)

def get_quotes(mood, n=3):
    filtered = df[df['sentiment_class'] == mood]
    if filtered.empty:
        return []
    cols = [c for c in ['Quote', 'Character', 'Anime'] if c in filtered.columns]
    return filtered.sample(n=min(n, len(filtered)))[cols].to_dict('records')


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
        if mood in ('positive', 'negative', 'neutral'):
            quotes = get_quotes(mood)
    return render_template('index.html', user=session['user'], mood=mood, quotes=quotes)


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
