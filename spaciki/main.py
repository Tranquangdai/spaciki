import pdb
from os.path import abspath, dirname, join

import spacy
from spacy.matcher import Matcher, PhraseMatcher
from spacy.tokens import Doc, Span, Token

from .patterns import patterns
from .utils import merge_matches


class attrs:
    _has_brand = 'has_brand'
    _brand = 'brand'
    _is_brand = 'is_brand'

    _is_model_type = 'is_model_type'
    _model_type = 'model_type'
    _has_model_type = 'has_model_type'

    _is_attributes = 'is_attributes'
    _attributes = 'attributes'
    _has_attributes = 'has_attributes'

    _is_quantity = 'is_quantity'
    _quantity = 'quantity'
    _has_quantity = 'has_quantity'

    _is_clothes_size = 'is_clothes_size'
    _clothes_size = 'clothes_size'
    _has_clothes_size = 'has_clothes_size'

    _dict = {
        'MODEL_TYPE': _is_model_type,
        'ATTRIBUTES': _is_attributes,
        'QUANTITY': _is_quantity,
        'CLOTHES_SIZE': _is_clothes_size
    }


class Spaciki:

    _ATTRS = ['brand', 'model_type', 'attributes', 'quantity', 'clothes_size']

    def __init__(self, nlp, force_extension=True):
        self.brand_matcher = PhraseMatcher(nlp.vocab, attr='LOWER')
        phrases_doc = [nlp.make_doc(doc) for doc in self._load_phrases()]
        self.brand_matcher.add('BRAND', None, *phrases_doc)

        for typ in self._ATTRS:
            Doc.set_extension(getattr(attrs, f'_has_{typ}'),
                              getter=getattr(self, f'has_{typ}'),
                              force=force_extension)
            Doc.set_extension(getattr(attrs, f'_{typ}'),
                              getter=getattr(self, f'iter_{typ}'),
                              force=force_extension)
            Span.set_extension(getattr(attrs, f'_has_{typ}'),
                               getter=getattr(self, f'has_{typ}'),
                               force=force_extension)
            Span.set_extension(getattr(attrs, f'_{typ}'),
                               getter=getattr(self, f'iter_{typ}'),
                               force=force_extension)
            Token.set_extension(getattr(attrs, f'_is_{typ}'), default=False,
                                force=force_extension)

        self.matcher = Matcher(nlp.vocab)
        for name, pattern in patterns:
            self.matcher.add(name, None, pattern)

    def _load_phrases(self):
        path = join(abspath(dirname(__file__)), 'data/brand_name.txt')
        with open(path, 'r') as f:
            phrases = f.read().split('\n')
        return phrases

    def __call__(self, doc):

        with doc.retokenize() as retokenizer:
            matches = self.brand_matcher(doc)
            temp_matches = sorted(matches, key=lambda x: (x[0], x[1], x[2]))
            temp_matches = merge_matches([{'label': match_id, 'start': l, 'end': r}
                                          for match_id, l, r in temp_matches])
            new_matches = [(each['label'], each['start'], each['end'])
                           for each in temp_matches]
            for _, start, end in new_matches:
                span = doc[start:end]
                for token in span:
                    token._.set(attrs._is_brand, True)
                retokenizer.merge(span)

            for match_id, start, end in self.matcher(doc):
                rule_name = self.matcher.vocab.strings[match_id]
                span = doc[start:end]
                for token in span:
                    token._.set(attrs._dict.get(rule_name), True)
                retokenizer.merge(span)

        return doc

    def has_brand(self, tokens):
        return self.has_(tokens, attrs._is_brand)

    def iter_brand(self, tokens):
        return self.iter_(tokens, attrs._is_brand)

    def has_model_type(self, tokens):
        return self.has_(tokens, attrs._is_model_type)

    def iter_model_type(self, tokens):
        return self.iter_(tokens, attrs._is_model_type)

    def has_attributes(self, tokens):
        return self.has_(tokens, attrs._is_attributes)

    def iter_attributes(self, tokens):
        return self.iter_(tokens, attrs._is_attributes)

    def has_quantity(self, tokens):
        return self.has_(tokens, attrs._is_quantity)

    def iter_quantity(self, tokens):
        return self.iter_(tokens, attrs._is_quantity)

    def has_clothes_size(self, tokens):
        return self.has_(tokens, attrs._is_clothes_size)

    def iter_clothes_size(self, tokens):
        return self.iter_(tokens, attrs._is_clothes_size)

    @staticmethod
    def has_(tokens, attrs_name):
        return any(token._.get(attrs_name) for token in tokens)

    @staticmethod
    def iter_(tokens, attrs_name):
        return [(tok.text, i) for i, tok in enumerate(tokens)
                if tok._.get(attrs_name)]


if __name__ == '__main__':
    nlp = spacy.load('en')
    spaciki = Spaciki(nlp)
    doc = spaciki(nlp.make_doc("Bộ Chữ Số Nam Châm Cho Bé 123 Antona"))
    print(doc._.brand)

    doc = spaciki(nlp.make_doc("Sáp mocha 30L Grasse LEsterel Bullsone 130g"))
    print(doc._.brand, doc._.model_type, doc._.attributes)
