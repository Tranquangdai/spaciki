patterns = [
    ('MODEL_TYPE',
        [{'TEXT': {
            'REGEX': r'([0-9]{0,2}[A-Z]{1,}[0-9]{1,}[A-Z]{0,}[0-9]{0,}[A-Z]{0,}[0-9]{0,})|([0-9]{4,})'}
          }]
     ),
    ('ATTRIBUTES',
        [{'TEXT': {
            'REGEX': r'(\s[0-9]{1,}\slít)|(\s[0-9]{1,4}(mAh|L|W|ml|l|g|kg|mm|cm|m|GB|V|Kg|HP))|(\s[0-9]{1,}(.|,)[0-9]{1,2}(mAh|L|W|ml|l|g|kg|mm|cm|m|mAh|GB|V|HP))|(\s[0-9]{1,}\s{1,}(inches|inch))'}
          }]
     )
]
