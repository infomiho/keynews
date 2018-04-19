from difflib import SequenceMatcher
from Levenshtein import distance
from .spacy_model_provider import get_model
from .summarization import summarize
from .named_entity_recognition import NER
from .extract_text import get_article
from .key_phrase_extraction import KeyPhraseExtraction
from .en_pronouns_prepositions import EN_PRONOUNS_PREPOSITIONS
from .blacklist import BLACKLISTED_KEYPHRASES

import re

class ArticleInfo:
    def top_keywords(self, doc):
        return sorted(doc, key=lambda x: x[1], reverse=True)[:5]

    def find_keywords(self, texts):
        corpus_tfidf, dictionary = self.kpe.rank_keyphrases_by_tfidf(texts)
        return [[dictionary[i] for (i, prob) in self.top_keywords(doc)] for doc in corpus_tfidf]

    def find_keyphrases_cached_tfidf(self, single_article):
        return self.kpe.rank_keyphrases_by_cached_tfidf(single_article)

    def NER_article(self, content, title=None):
        entities = self.ner.extract(content)
        if title:
            entities = entities.union(self.ner.extract(title))
        return entities

    def download_article(self, article):
        return get_article(article.link)

    def process_article(self, article):
        summary = summarize(article)

        summary_entities = self.NER_article(summary, article.title)
        # entities = self.NER_article(article['content'], article['title'])

        top_keyphrases = set(self.find_keyphrases_cached_tfidf(article))

        kpe = [kp for kp in summary_entities | top_keyphrases if self.is_valid_candidate(kp)]
        self.filter_similar(kpe)
        return {'title': article.title, 'summary': summary, 'keyphrases_entites': kpe}

    def keywords_similar (self, keyword1, keyword2, min_le_nc=0.84, min_sm_nc=0.84, min_sm_c=0.5):
        a = keyword1.lower()
        b = keyword2.lower()
        sim_sm = SequenceMatcher(a=a, b=b).ratio()
        sim_le = 1 - distance(a, b) / max(len(a), len(b))
        contains = a in b or b in a
        return contains and sim_sm > min_sm_c \
               or sim_sm > min_sm_nc and sim_le > min_le_nc

    def filter_similar(self, keyphrases):
        to_remove = set()
        for i in range(0, len(keyphrases)):
            for j in range(0, i):
                if self.keywords_similar(keyphrases[i], keyphrases[j]):
                    to_remove.add(keyphrases[j])
        for duplicate in to_remove:
            keyphrases.remove(duplicate)

    def is_valid_candidate(self, candidate):
        return candidate.split()[0] not in EN_PRONOUNS_PREPOSITIONS \
                and candidate.lower() not in BLACKLISTED_KEYPHRASES \
                and len(candidate) > 2 \
                and not candidate.isdigit() \
                and len(re.findall('^\\(?-?\\s*\\d+(\\.\\d+)?\\s*(%|per\\s*cent)?\\)?$', candidate)) == 0 \
                and len(re.findall('^[@\']', candidate)) == 0 \
                and len(re.findall('[\(\)\|\",\\/]', candidate)) == 0

    def __init__(self):
        self.ner = NER()
        self.kpe = KeyPhraseExtraction()
