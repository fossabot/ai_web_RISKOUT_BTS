# NLP-Tools for riskout

## Quick Demo

1. Update/install Docker and build & run

```bash
curl -fsSL https://get.docker.com/ | sudo sh

# Build dockerfile!
docker build --tag nlptools:1.0 .

# Run image and bash
docker run --rm -p 8000:8000 nlptools:1.0
```

2. Go to {your_domain_or_ip_address}/docs and see API Docs

## How to use NLP-Tools

1. Use as Python packages
2. Use as REST-API Server

### 1) SUMMARIZER

- `POST` `/summarize`

```json
// REQUEST
{
  "document": "SK이노베이션이 임시 주주총회을 열고 배터리 사업 분사를 결의했다. SK이노베이션은 16일 오전 10시 서울 종로구 SK서린빌딩에서 임시 주주총회를 열고 'SK배터리 주식회사(가칭)'와 'SK E&P 주식회사(가칭)'의 물적분할안을 의결했다. 전 체 주주의 74.57%(6233만1624주)가 주총에 참석했으며, 이 가운데 80.2%(4998만1081주)가 찬성했다. 분할 조 건인 주총 참석 주식의 3분의 2 이상, 전체 주식의 3분의 1이상 찬성을 확보했다. 2대 주주인 국민연금이 분 사안에 반대한다는 의사를 밝혔지만 글로벌 의결권 자문기구 등이 찬성 의사를 밝혔다. SK이노베이션의 지분 율은 올해 반기 기준 ㈜SK 등 특수관계인 33.4%, SK이노베이션 자기주식 10.8%, 국민연금 8.1%, 기타(외국인 및 국내 기관, 개인주주) 47.7% 등이다. 기타 지분 중 외국인ㆍ국내 기관이 약 26%, 개인주주가 22% 수준이다."
}

// RESPONSE
{
    "summairzed": "SK이노베이션은 16일 오전 10시 서울 종로구 SK서린빌딩에서 임시 주주총회를 열고 'SK배터리 주식회사(가칭)'와 'SK E&P 주식회사(가칭)'의 물적분할안을 의결했다.",
    "time": 5.45867395401001
}
```

### 2) TEXTRANK

- `POST` `/textrank`

```json
// REQUEST

