from typing import List, Any
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModel, AutoModelForSeq2SeqLM
from datetime import datetime
from pydantic import BaseModel

# Словарь для маппинга индексов на категории
id2label = {
    0: 'climate', 1: 'conflicts', 2: 'culture', 3: 'economy', 4: 'gloss',
    5: 'health', 6: 'politics', 7: 'science', 8: 'society', 9: 'sports', 10: 'travel'
}

class NewsItem(BaseModel):
    url: str
    date: datetime
    news: str
    links: str
    agency: str
    title: str = ""
    resume: str = ""
    embedding: List[float] = []
    category: str = ""

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def get_classifier_model():
    model_name = "data-silence/any-news-classifier"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name).to(device)
    return CategoryModel(model=model, tokenizer=tokenizer, device=device, id2label=id2label)

def get_embedding_model():
    model_name = "sentence-transformers/LaBSE"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    return EmbeddingModel(model=model, tokenizer=tokenizer, device=device)


def get_headline_model():
    model_name = "IlyaGusev/rut5_base_headline_gen_telegram"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    return HeadlineModel(model=model, tokenizer=tokenizer, device=device)

def get_summary_model():
    model_name = "IlyaGusev/mbart_ru_sum_gazeta"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name).to(device)
    return SummaryModel(model=model, tokenizer=tokenizer, device=device)



class ModelInterface:
    def __init__(self, model, tokenizer, device):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device

    async def process(self, texts: List[str]) -> List[Any]:
        raise NotImplementedError

class EmbeddingModel(ModelInterface):
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        inputs = self.tokenizer(texts, return_tensors="pt", padding=True, truncation=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
        embeddings = outputs.pooler_output
        embeddings = torch.nn.functional.normalize(embeddings, dim=1)
        return embeddings.cpu().tolist()

class CategoryModel(ModelInterface):
    def __init__(self, model, tokenizer, device, id2label):
        super().__init__(model, tokenizer, device)
        self.id2label = id2label

    async def predict_categories(self, texts: List[str]) -> List[str]:
        inputs = self.tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512).to(self.device)
        with torch.no_grad():
            outputs = self.model(**inputs)
            logits = outputs.logits

        predicted_labels = torch.argmax(logits, dim=-1).tolist()
        return [self.id2label[label] for label in predicted_labels]

class HeadlineModel(ModelInterface):
    async def process(self, texts: List[str]) -> List[str]:
        titles = []
        for text in texts:
            input_ids = self.tokenizer(
                [text],
                max_length=600,
                add_special_tokens=True,
                padding="max_length",
                truncation=True,
                return_tensors="pt"
            )["input_ids"].to(self.device)


            output_ids = self.model.generate(input_ids=input_ids)[0]
            headline = self.tokenizer.decode(output_ids, skip_special_tokens=True)
            titles.append(headline)
        return titles

class SummaryModel(ModelInterface):
    async def process(self, texts: List[str]) -> List[str]:
        summaries = []
        for text in texts:
            input_ids = self.tokenizer(
                [text],
                max_length=600,
                padding="max_length",
                truncation=True,
                return_tensors="pt",
            )["input_ids"].to(self.device)

            output_ids = self.model.generate(
                input_ids=input_ids,
                no_repeat_ngram_size=4
            )[0]

            summary = self.tokenizer.decode(output_ids, skip_special_tokens=True)
            summaries.append(summary)
        return summaries

# Инициализация моделей
# embedder = EmbeddingModel(embedding_model, embedding_tokenizer, device)
# categorizer = CategoryModel(category_model, category_tokenizer, device, id2label)
# headliner = HeadlineModel(headline_model, headline_tokenizer, device)
# summarizer = SummaryModel(summary_model, summary_tokenizer, device)