# Keynews

## Objective
Our objective was to enable the end user to explore current news space and deduce connections between key phrases. It included downloading currently trending news stories from multitude of news outlets.
We approached this objective from a standpoint of a connected graph where the nodes represent the keyphrases and the edges represent the connections.

## How we solved it

We created a system that would scrape article links from newsapi.org, downloaded them and finally process them with our NLP pipeline. Our NLP pipeline consisted out of:
- Named entity recognition
- Keyphrase extraction
- Keyphrase ranking using TF-IDF
- Text summarization using TextRank
- Finding colocated keyphrases in articles

## Technologies used
- Python 3.6
- Flask
- SQLAlchemy
- APScheduler
  - Scheduled background article fetching and processing 
- SpaCy
  - Named entity recognition
  - Parts-of-speech tagging 
- Gensim
  - TF-IDF keyphrase ranking
  - TextRank text summarization
- Cytoscape.js / React
  - Graph visualisation

## People involved

- Mate Mijolović
- Ivan Dujmić
- Mihovil Ilakovac

Project done [@Takelab](http://takelab.fer.hr/) - 2017
