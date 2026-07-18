FROM mageai/mageai:latest

WORKDIR /home/src

COPY requirements.txt .

RUN pip install --default-timeout=10000 -r requirements.txt

COPY . .

EXPOSE 6789

CMD ["mage", "start", "marinetraffic"]