import pdb

import spacy
from spaciki.main import Spaciki


def test():
    nlp = spacy.load('en', disables=['ner', 'parser'])
    nlp.add_pipe(Spaciki(nlp), first=True)

    doc = nlp("Kem tan mỡ, thon gọn - Super Clean Soap Sculpture")
    assert doc[7]._.is_brand == True
    assert doc._.has_brand == True
    assert doc._.brand == [('Super Clean Soap', 7)]

    doc = nlp("Tranh khung Thế Giới Tranh Đẹp KWT50110 35 x 50 cm")
    assert doc._.model_type == [('KWT50110', 3)]
    assert doc[3]._.is_model_type == True

    doc = nlp("Lò vi sóng có nướng Sharp RG223VNSM 20L")
    print(doc._.model_type)
    assert doc._.model_type
    assert doc._.attributes
