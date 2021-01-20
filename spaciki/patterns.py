METRICS = ["mAh", "L", "W", "ml", "l", "g", "kg", "mm", "cm",
           "m", "GB", "V", "Kg", "HP", "lít", "inch", "inches"]
UNIT = ['tờ', 'miếng', 'cái', 'bìa', 'chiếc', 'cuộn', 'gói', 'túi',
        'chấu', 'cốc', 'màu', 'bữa', 'trang', 'ly', 'cây', 'món', 'chai',
        'bánh', 'tầng', 'bút', 'chỗ', 'nước', 'mảnh', 'ngăn', 'hộp']

patterns = [
    (
        'MODEL_TYPE',
        [{'TEXT': {
            'REGEX': r'([0-9]{0,2}[A-Z]{1,}[0-9]{1,}[A-Z]{0,}[0-9]{0,}[A-Z]{0,}[0-9]{0,})|([0-9]{4,})'}
          }]
    ),
    (
        'ATTRIBUTES',
        [
            {'TEXT': {'LEMMA': 'IS_DIGIT'}},
            {'TEXT': {'IN': METRICS}}
        ]
    ),
    (
        'ATTRIBUTES',
        [
            {'TEXT': {'REGEX': r'[0-9]{1,}(.|,)[0-9]{1,2}'}},
            {'TEXT': {'IN': METRICS}}
        ]
    ),
    (
        'ATTRIBUTES',
        [
            {'TEXT':
             {'REGEX':
              '^[0-9]{1,4}(mAh|L|W|ml|l|g|kg|mm|cm|m|GB|V|Kg|HP|lít|inch|inches)$'}}
        ]
    ),
    (
        'QUANTITY',
        [
            {'TEXT': {'LEMMA': 'IS_DIGIT'}},
            {'LOWER': {'IN': UNIT}}
        ]
    ),
    (
        'CLOTHES_SIZE',
        [
            {'TEXT': {'REGEX': '^(S|M|X|XX|XXL)[0-9]{1,2}$'}}
        ]
    )
]
