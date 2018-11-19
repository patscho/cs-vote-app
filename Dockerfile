FROM python:3.6-alpine
ADD app /app
RUN pip3 install -r app/requirements.txt
WORKDIR /app
CMD [ "python", "poll.py" ]
