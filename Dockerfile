FROM python:3.8.10-slim

COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip \
	&& pip install -r requirements.txt \
	&& rm -rf ~/.cache/pip
	
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENV ORIGIN="127.0.0.1:5100" PORT="5100" PREFIX=""

COPY ./app /app
ENTRYPOINT ["./entrypoint.sh"]
