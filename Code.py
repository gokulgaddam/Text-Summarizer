!git clone https://github.com/Jcharis/NLP-Web-Apps.git

cd NLP-Web-Apps/Summaryzer_Text_Summarization_App/

!pip install beautifulsoup4==4.7.0 
!pip install bs4==0.0.1  
!pip install Flask==1.0.2
!pip install nltk==3.4 
!pip install spacy==2.0.18   
!pip install sumy==0.7.0 
!pip install thinc==6.12.1 
!pip install urllib3==1.24.1
!pip install gensim==3.6.0 
!pip install gensim-sum-ext==0.1.2
!pip install flask-ngrok
!pip install sumbert
!pip install bert-extractive-summarizer
!pip install transformers==2.2.2
!pip install neuralcoref
!python -m spacy download en_core_web_lg
!python -m spacy link en_core_web_lg en
!python -m spacy download en_core_web_sm

!npm install -g localtunnel

!python app.py

from __future__ import unicode_literals
from flask import Flask,render_template,url_for,request


from flask_ngrok import run_with_ngrok
from summarizer import Summarizer    ''' Extractive bert '''
from sumbert import summarize        ''' Abstractive bert '''
from flask import Flask
import time
import spacy
nlp = spacy.load('en')
app = Flask(__name__)
run_with_ngrok(app)  

# Web Scraping Pkg
from bs4 import BeautifulSoup
from urllib.request import urlopen
#from urllib import urlopen
model=Summarizer()



# Reading Time
def readingTime(mytext):
	total_words = len([ token.text for token in nlp(mytext)])
	estimatedTime = total_words/200.0
	return estimatedTime

# Fetch Text From Url
def get_text(url):
	page = urlopen(url)
	soup = BeautifulSoup(page)
	fetched_text = ' '.join(map(lambda p:p.text,soup.find_all('p')))
	return fetched_text

@app.route('/')
def index():
	return render_template('index.html')


@app.route('/analyze',methods=['GET','POST'])
def analyze():
	start = time.time()
	if request.method == 'POST':
		rawtext = request.form['rawtext']
		final_reading_time = readingTime(rawtext)
		final_summary = model(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)

@app.route('/analyze_url',methods=['GET','POST'])
def analyze_url():
	start = time.time()
	if request.method == 'POST':
		raw_url = request.form['raw_url']
		rawtext = get_text(raw_url)
		final_reading_time = readingTime(rawtext)
		final_summary = model(rawtext)
		summary_reading_time = readingTime(final_summary)
		end = time.time()
		final_time = end-start
	return render_template('index.html',ctext=rawtext,final_summary=final_summary,final_time=final_time,final_reading_time=final_reading_time,summary_reading_time=summary_reading_time)







@app.route('/about')
def about():
	return render_template('index.html')

if __name__ == '__main__':
	app.run()
