import pdb

import spacy
from spaciki import Spaciki


def test():
    nlp = spacy.load('en', disables=['ner', 'parser'])
    nlp.add_pipe(Spaciki(nlp), first=True)

    doc = nlp("Kem tan mỡ, thon gọn - super clean soap Sculpture")
    assert doc[7]._.is_brand is True
    assert doc._.has_brand is True
    assert doc._.brand == [('super clean soap', 7)]

    doc = nlp("Tranh khung Thế Giới Tranh Đẹp KWT50110 35 x 50 cm")
    assert doc._.model_type == [('KWT50110', 3)]
    assert doc[3]._.is_model_type is True

    doc = nlp("Lò vi sóng có nướng Sharp RG223VNSM 20L")
    assert doc._.model_type == [('RG223VNSM', 6)]
    assert doc._.attributes == [('20L', 7)]

    doc = nlp("Quần áo trẻ em XXL23")
    assert doc._.clothes_size == [('XXL23', 4)]

    doc = nlp("Combo 3 tờ giấy học sinh")
    assert doc._.quantity == [('3 tờ', 1)]
