"""
일단은 generator를 통해 json 파일들을 다루는 것으로 하게 됐다.
이유는 어쩌다 보니까 이렇게 돼 버렸다 ㅎ
항목의 이름을 바꾸는 것은 매우 큰 비용을 낳고 잠재적 버그를 키울 수 있으니 가급적(절대) 하지 말 것
"""

import json
import sys
import os

def make_file(config, name):
    path= os.path.dirname(os.path.abspath(__file__))
    sys.stdout = open(path + f'/{name}.txt','w')
    print(json.dumps(config, indent=4))
    sys.stdout.close()

def navernews_generator():
    naver = {
        'name': 'naver', \
        'title' : [{'div': 'div', 'div_class': 'article_info', 'tag': 'h3'}],\
        'body' : [{'div': 'div', 'div_class': '_article_body_contents'}],\
        'img' : [{'div': 'span', 'div_class': 'end_photo_org'}]
    }
    
    make_file(naver, 'naver')

def naverlist_generator():
    naver = {
        'name': 'naverlist',\
        'list': [{'div': 'div', 'div_class': 'list_body newsflash_body'}]
    }

    make_file(naver, 'naverlist')



# navernews_generator()
# naverlist_generator()