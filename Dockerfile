FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    net-tools \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Talablar faylini qo‘shish va pip o‘rnatish
COPY requirements.txt .
RUN pip install -r requirements.txt

# Django loyihasini qo‘shish
COPY . .

# Portni ochish
EXPOSE 8005

# Django serverini ishga tushirish
CMD ["python", "manage.py", "runserver", "0.0.0.0:8005"]
