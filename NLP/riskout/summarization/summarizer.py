import torch
from kobart import get_kobart_tokenizer
from transformers.models.bart import BartForConditionalGeneration

from functools import wraps
import errno
import os
import signal


class TimeoutError(Exception):
    def __init__(self, error_msg):
        self.msg = f"Timeout error occured : {error_msg}"

    def __str__(self):
        return self.msg


def timeout(seconds=20, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL,seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result
        return wraps(func)(wrapper)
    return decorator


class KorbartSummarizer:
    def __init__(self, model_path, tokenizer=get_kobart_tokenizer, max_length=1024, num_beams=10):
        self.model = BartForConditionalGeneration.from_pretrained(model_path)
        self.tokenizer = tokenizer()
        self.max_length = max_length
        self.num_beams = num_beams

    def _preprocess(self, text: str):
        sents = text.replace('\n', '')
        input_ids = self.tokenizer.encode(sents, max_length=1024, truncation=True)
        input_ids = torch.tensor(input_ids).unsqueeze(0)
        return input_ids

    @timeout(20)
    def predict(self, text: str):
        try:
            input_ids = self._preprocess(text)
            output = self.model.generate(input_ids, eos_token_id=1,
                                        max_length=self.max_length, num_beams=self.num_beams)
            output = self.tokenizer.decode(output[0], skip_special_tokens=True)

        except TimeoutError as e:
            return e
            
        return output
