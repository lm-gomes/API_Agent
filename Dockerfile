FROM python:3.12
WORKDIR /usr/local/app

RUN pip install -U langchain
RUN pip install -U langgraph
RUN pip install -U langchain-groq
RUN pip install fastapi
RUN pip install uvicorn
ENV GROQ_API_KEY={your_api_key}
COPY . .

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]