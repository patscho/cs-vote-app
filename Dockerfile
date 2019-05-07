FROM python:3.6-alpine
ADD app/requirements.txt /app/requirements.txt
RUN pip3 install -r app/requirements.txt
ADD app /app
WORKDIR /app
CMD [ "python", "poll.py" ]
