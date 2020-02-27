FROM python:3.7-slim-buster

ENV http_proxy http://proxy.cat.com:80
ENV https_proxy http://proxy.cat.com:80
ENV no_proxy localhost,ap.cat.com

ADD requirements.txt ./
ADD dist/*.whl ./

RUN python3 -m pip install -r requirements.txt
RUN python3 -m pip install *.whl