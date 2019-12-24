FROM python:3.6.7
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
RUN mkdir /fundoo
WORKDIR /fundoo
ADD . /fundoo/
RUN apt-get update
RUN apt-get install build-essential libssl-dev libffi-dev python3-dev -y
RUN pip install -r requirements.txt
CMD ["python", "./manage.py runserver 0.0.0.0:8000"]