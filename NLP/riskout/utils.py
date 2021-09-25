from konlpy.tag import Okt, Komoran, Mecab, Hannanum, Kkma


def get_tokenizer(tokenizer_name):
    if tokenizer_name == "komoran":
        tokenizer = Komoran()
    elif tokenizer_name == "okt":
        tokenizer = Okt()
    elif tokenizer_name == "mecab":
        tokenizer = Mecab()
    elif tokenizer_name == "hannanum":
        tokenizer = Hannanum()
    elif tokenizer_name == "kkma":
        tokenizer = Kkma()
    else:
        tokenizer = Mecab()
    return tokenizer


def tokenize(tokenizer, sent):
    words = tokenizer.nouns(sent)
    words = [w for w in words]
    return words