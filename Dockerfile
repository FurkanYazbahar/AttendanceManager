# Python 3.13 temel imajı
FROM python:3.13-slim

# Ortam değişkenlerini ayarla
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Çalışma dizinini ayarla
WORKDIR /app

# Sistem bağımlılıklarını yükle
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    python3-dev \
    wget \
    && apt-get clean

# pip'i güncelle
RUN pip install --upgrade pip

# Gereksinim dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Proje dosyalarını kopyala
COPY . /app/

# Portu aç
EXPOSE 8000

# Uygulamayı başlat
CMD ["sh", "-c", "python manage.py migrate && python manage.py seed && python manage.py runserver 0.0.0.0:8000"]
