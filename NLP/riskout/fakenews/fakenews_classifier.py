import torch
import torch.nn.functional as F
from riskout.fakenews.utils import get_tokenizer
from typing import List, Union, Optional, Callable


class FakeNewsClassifier:
    """ SenCNN Fakenews classifier 
    
    Args:
        vocab_path (str): path for vocab pickle file
        model_path (str): pt file path for SenCNN trained model
        split_morphs (Callable[str, List[str]]): split sentence to morphs chunks
    """ 
    def __init__(self, vocab_path, model_path, split_morphs):
        self.model = torch.load(model_path)
        self.split_morphs = split_morphs
        self.tokenizer = get_tokenizer(vocab_path, split_morphs)

    def predict(self, texts: Union[List[str],str]):
        """Return probability of being true"""    
        if isinstance(texts, str):
            texts = [texts]

        with torch.no_grad():
            X = torch.tensor([[self.tokenizer.split_and_transform(text)] for text in texts])
            y_hat = self.model(X)
            prob = F.softmax(y_hat, dim=1)[0]
        return prob[1]

