FROM python:3.10-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# RUN pip install --upgrade pip
#copy to code directory
COPY . /code 

#set permissions


RUN chmod +x /code
WORKDIR /code

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8005
CMD pip uninstall flask -y
CMD pip install flask

CMD pip install -e .

CMD ["python","app.py"]