import re
from emoji import EMOJI_DATA
from api.news.phrase_dict import black_labels
import unicodedata


class TextCleaner:
    def __init__(self):
        self.black_labels = black_labels

    def clean_news(self, news: str, channel: str | None = None) -> str:
        """Очищает новость от мусора согласно настройкам словаря black_labels."""
        total_label = {*self.black_labels['common_labels']}
        if channel in self.black_labels:
            total_label |= {*self.black_labels[channel]}

        for label in total_label:
            news = news.replace(label, ' ')

        news = self._clean_text(news)
        news = self._remove_urls(news)
        news = self._remove_hashtags_and_mentions(news)

        return re.sub(" +", " ", news).strip()

    @staticmethod
    def _clean_text(text: str) -> str:
        """Очищает текст от эмодзи и специальных символов."""
        # Удаление эмодзи и основных специальных символов
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # эмодзи эмоций
                                   u"\U0001F300-\U0001F5FF"  # символы и пиктограммы
                                   u"\U0001F680-\U0001F6FF"  # транспорт и символы карт
                                   u"\U0001F1E0-\U0001F1FF"  # флаги (iOS)
                                   u"(\U0001F1F2\U0001F1F4)"  # Macau flag
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   "]+", flags=re.UNICODE)

        text = emoji_pattern.sub(r'', text)

        # Удаление специальных пробельных символов
        text = re.sub(r'[\u00A0\u2000-\u200A\u2028\u2029\u202F\u205F\u3000\uFEFF]', ' ', text)

        # Удаление специальных внутритекстовых символов
        text = re.sub(r'[\u200B\u200C\u200D\u200E\u200F\u202A\u202B\u202C\u202D\u202E\xa0]', '', text)

        # Нормализация текста (замена составных символов на их базовые эквиваленты)
        text = unicodedata.normalize('NFKD', text)

        # Удаление всех управляющих символов, кроме обычных пробелов, и оставшихся эмоджи
        text = ''.join(char for char in text if unicodedata.category(char)[0] != 'C' or char == ' ')
        text = ''.join(char for char in text if char not in EMOJI_DATA)
        # text = text.replace('\n', ' ').replace('\t', ' ')
        # Удаляем эмоджи и другие нежелательные символы
        # text = re.sub(r'[^\w\s\p{P}]', '', text, flags=re.UNICODE)

        # Замена множественных пробелов на один
        text = re.sub(r'\s+', ' ', text)

        return text.strip()

    @staticmethod
    def _remove_urls(text: str) -> str:
        """Удаляет URL-адреса из текста."""
        text = re.sub("https?://[-/_.a-zA-Z0-9]*.[-/_.a-zA-Z]*/[-/_.a-zA-Z0-9]*$", " ", text)
        text = re.sub("https://t.me/[/-_a-zA-Z0-9]*$", " ", text)
        text = re.sub("(go.vc.ru|vc.ru)/[-/_.a-zA-Z0-9]*", " ", text)
        return text

    @staticmethod
    def _remove_hashtags_and_mentions(text: str) -> str:
        """Удаляет хэштеги и упоминания из текста."""
        text = re.sub("#[а-яА-Я]*$", " ", text)
        text = re.sub("@[a-zA-Z]*$", " ", text)
        return text
