FROM python:3

WORKDIR /core

ENV PATH /root/.local/bin:$PATH

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .