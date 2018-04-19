from .spacy_model_provider import get_model


class NER:
    def extract(self, content):
        nlp = get_model()
        doc = nlp(content)
        entities = set([])
        for chunk in doc.noun_chunks:
            for ent in doc.ents:
                if ent.text == chunk.text and ent.label_ in self.allowed_entity_types:
                    entities.add(chunk.text.replace('\n', ''))
        return entities

    def __init__(self):
        self.allowed_entity_types = set(['PERSON', 'ORG', 'GPE'])
