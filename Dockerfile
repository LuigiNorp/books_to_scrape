# Version: 0.0.1

FROM python:3.8
RUN apt-get update && apt-get upgrade -y
RUN pip install --upgrade pip
RUN pip install scrapy
RUN pip install pillow
COPY BookScrapper BookScrapper
WORKDIR /BookScrapper