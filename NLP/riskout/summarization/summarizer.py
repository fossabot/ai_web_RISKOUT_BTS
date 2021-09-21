import torch
from .tokenization_kobert import KoBertTokenizer
from transformers.models.bart import BartForConditionalGeneration


class KorbartSummarizer:
    def __init__(self, model_path, tokenizer=None, max_length=2048, num_beams=10):
        self.model = BartForConditionalGeneration.from_pretrained(model_path)
        self.tokenizer = tokenizer or KoBertTokenizer.from_pretrained('monologg/kobert')
        self.max_length = max_length
        self.num_beams = num_beams

    def _preprocess(self, text):
        sents = text.replace('\n', '')
        input_ids = self.tokenizer.encode(sents)
        input_ids = torch.tensor(input_ids)
        input_ids = input_ids.unsqueeze(0)
        return input_ids

    def predict(self, text):
        input_ids = self._preprocess(text)
        output = self.model.generate(input_ids, eos_token_id=1,
                                     max_length=self.max_length, num_beams=self.num_beams)
        output = self.tokenizer.decode(output[0], skip_special_tokens=True)
        return output
