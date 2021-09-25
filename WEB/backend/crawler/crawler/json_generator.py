"""
일단은 generator를 통해 json 파일들을 다루는 것으로 하게 됐다.
이유는 어쩌다 보니까 이렇게 돼 버렸다 ㅎ
항목의 이름을 바꾸는 것은 매우 큰 비용을 낳고 잠재적 버그를 키울 수 있으니 가급적(절대) 하지 말 것
"""

import json
import sys
import os

def make_file(config, dir, name):
    path= os.path.dirname(os.path.abspath(__file__))
    sys.stdout = open(path + f'/{dir}/{name}.json','w')
    print(json.dumps(config, indent=4))
    sys.stdout.close()

def navercontents_generator():
    naver = {
        'name': 'contents',
        'title' : {'div': 'div', 'div_class': 'article_info', 'tag': 'h3'},
        'body' : {'div': 'div', 'div_class': '_article_body_contents'},
        'img' : {'div': 'span', 'div_class': 'end_photo_org'}
    }
    
    make_file(naver, 'naver', 'navernews')

def naverlist_generator():
    naver = {
        'name': 'list',
        'list': {'div': 'div', 'div_class': 'list_body newsflash_body'},
        'paging': {'div': 'div', 'div_class': 'paging', 'tag': 'strong'}
    }

    make_file(naver, 'naver', 'naverlist')

def DCcontents_generator():
    dc = {
        'name': 'contents', 
        'title': {'div': 'h3', 'div_class': 'title ub-word', 'tag': 'span', 'tag_class': 'title_subject'},
        'body': {'div': 'div', 'div_class': 'write_div'}
    }
    make_file(dc, 'dcinside', 'dccontents')

def DClist_generator():
    dc = {
        'name': 'list',
        'list': {'div': 'tbody'},
        'paging': {'div': 'div', 'div_class': 'bottom_paging_box', 'tag': 'em'}
    }
    make_file(dc, 'dcinside', 'dclist')

# Naver
# navernews_generator()
# naverlist_generator()

# DC
# DCcontents_generator()
# DClist_generator()