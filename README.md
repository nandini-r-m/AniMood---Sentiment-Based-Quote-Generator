Anime Quote Generator

A Flask-based web application that recommends anime quotes based on the user’s mood using sentiment analysis. The app analyzes quotes from popular anime series and displays motivational, emotional, or neutral quotes dynamically.

**Features**
1. Mood-based anime quote recommendations  
2. Sentiment analysis using VADER Sentiment Analyzer  
3. Simple login authentication system  
4. Random quote generation  
5. Anime quotes dataset stored in JSON format  
6. Flask-powered web application  
7. Clean and responsive UI  
  
**Tech Stack**  
Backend: Python, Flask  
Frontend: HTML, CSS  
Data Processing: Pandas  
Sentiment Analysis: VADER Sentiment  
Dataset Format: JSON  
  
**Installation**  
1. Clone the repository  
git clone https://github.com/your-username/quote-generator.git  
cd quote-generator  
2. Create a virtual environment  
python -m venv venv  
3. Activate the virtual environment  
Windows
venv\Scripts\activate
Mac/Linux
source venv/bin/activate  
4. Install dependencies  
pip install -r requirements.txt
Run the Application
python app.py

Open your browser and go to:  

http://127.0.0.1:5000
**Login Credentials**  
Username: admin
Password: password
  
or
  
Username: demo
Password: demo
**How It Works**  
The app loads anime quotes from AnimeQuotes.json
Quotes are preprocessed and analyzed using VADER sentiment analysis
Quotes are classified into:
Positive
Neutral
Negative
Users select a mood
The app displays matching anime quotes randomly
_**Example Quotes**_  

“People’s lives don’t end when they die, it ends when they lose faith.” — Itachi Uchiha

“If you don’t take risks, you can’t create a future!” — Monkey D. Luffy

“Hard work is worthless for those that don’t believe in themselves.” — Naruto Uzumaki
