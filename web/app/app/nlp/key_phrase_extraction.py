import pickle
import gensim

from .spacy_model_provider import get_model, get_stopwords_set


class KeyPhraseExtraction:

    def __init__(self) -> None:
        super().__init__()
        self.dictionary = pickle.load(open('dictionary.pickle', 'rb'))
        self.tfidf_model = pickle.load(open('tfidf.pickle', 'rb'))


    def extract_candidate_chunks(self, content):
        # noun chunks extraction
        nlp = get_model()
        doc = nlp(content)

        adjectives_adverbs = set([token.text for token in doc if token.pos_ in {'ADJ', 'ADV'}])


        stopwords = get_stopwords_set()

        candidates = set([chunk.text.replace('\n', ' ') for chunk in doc.noun_chunks
                                    if chunk.text.lower() not in stopwords
                                    and chunk.text not in adjectives_adverbs])

        return candidates

    def generate_tfidf (self, articles):
         # extract candidate chunks from each text in texts
        candidates_by_texts = [self.extract_candidate_chunks(
            article.title + ". " + article.content) for article in articles]

        # make gensim dictionary and corpus
        dictionary = gensim.corpora.Dictionary(candidates_by_texts)
        corpus = [dictionary.doc2bow(candidate)
                  for candidate in candidates_by_texts]

        # transform corpus with tf*idf model
        tfidf = gensim.models.TfidfModel(corpus)
        return tfidf, dictionary

    def rank_keyphrases_by_tfidf(self, articles):
        # extract candidate chunks from each text in texts
        candidates_by_texts = [self.extract_candidate_chunks(
            article.title + ". " + article.content) for article in articles]

        # make gensim dictionary and corpus
        dictionary = gensim.corpora.Dictionary(candidates_by_texts)
        corpus = [dictionary.doc2bow(candidate)
                  for candidate in candidates_by_texts]

        # transform corpus with tf*idf model
        tfidf = gensim.models.TfidfModel(corpus)
        corpus_tfidf = tfidf[corpus]

        return corpus_tfidf, dictionary

    def rank_keyphrases_by_cached_tfidf(self, single_article):
        text = single_article.title + '. ' + single_article.content
        candidates = self.extract_candidate_chunks(text)

        article_bow = self.dictionary.doc2bow(candidates)
        article_tfidf = self.tfidf_model[[article_bow]]

        top_keyphrase_indexes = sorted(article_tfidf[0], key=lambda x: x[1], reverse=True)[:5]

        return [self.dictionary[i] for (i, prob) in top_keyphrase_indexes]

