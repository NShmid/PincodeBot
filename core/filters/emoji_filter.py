import re

from aiogram.types import Message


class TextNormalizer:
    def __init__(self, target_text=''):
        self.target_text = target_text.lower()
        
    def __call__(self, text: str) -> bool:
        return self.normalize(text) == self.target_text
        
    @staticmethod
    def normalize(text: str) -> str:
        text = re.sub(r'[^a-zA-Zа-яА-Я0-9\s]', '', text).lower().strip()
        return re.sub(r'\s+', ' ', text)