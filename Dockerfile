# 1
FROM python:3.7

# 2
WORKDIR /src
COPY app ./app
COPY migrations ./migrations
COPY .env gunicorn.conf.py requirements.txt run_gunicorn.sh ./
RUN chmod +x run_gunicorn.sh

# 3
RUN pip install -r requirements.txt

# 4
ENV PORT 8080
RUN curl --create-dirs -o $HOME/.postgresql/root.crt -O https://cockroachlabs.cloud/clusters/1e8ee25a-e1f5-4154-9e45-baa723da0b13/cert

# 5
CMD exec ./run_gunicorn.sh