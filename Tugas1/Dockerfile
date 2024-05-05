FROM python:3.10-slim-buster

WORKDIR /mysite

COPY requirements.txt ./

RUN pip install --no-cache-dir --upgrade pip \ 
    && pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "manage.py", "runserver", "0.0.0.0:5000"]