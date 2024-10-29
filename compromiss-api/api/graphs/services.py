import pymorphy3
from stop_words import get_stop_words


morph = pymorphy3.MorphAnalyzer()
stop_words = get_stop_words('russian')
stop_words.extend(['что', 'это', 'так',
                   'вот', 'быть', 'как',
                   'в', '—', 'к', 'за', 'из', 'из-за',
                   'на', 'ок', 'кстати',
                   'который', 'мочь', 'весь',
                   'еще', 'также', 'свой',
                   'ещё', 'самый', 'ул', 'комментарий',
                   'английский', 'язык', 'года', 'году', 'россия', 'рф', 'российский', 'россиянин', 'год'])


def normalize_row(row):
    words = row.split()
    normalized_words = []
    for word in words:
        if word.lower() not in stop_words:
            parsed = morph.parse(word)[0]
            normalized_word = parsed.normal_form
            normalized_words.append(normalized_word)
    return ' '.join(normalized_words)
