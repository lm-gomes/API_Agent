FROM python:3.12
WORKDIR /usr/local/app

RUN pip install -U langchain
RUN pip install -U langgraph
RUN pip install -U langchain-groq
ENV GROQ_API_KEY={your_api_key}

COPY . .

CMD ["python", "main.py"]