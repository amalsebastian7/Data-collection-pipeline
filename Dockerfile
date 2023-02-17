FROM python:3.7.13

WORKDIR /workdir
VOLUME ["/workdir"]

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "scrapper.py" ]
