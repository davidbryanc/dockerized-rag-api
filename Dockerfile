# Tahap 1: "Builder" - Gunakan image Python penuh yang berisi build tools.
# Ini akan secara drastis mempercepat proses pip install untuk paket yang butuh kompilasi.
FROM python:3.11 AS builder

# Set environment variables untuk pip
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Buat virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Upgrade pip terlebih dahulu
RUN pip install --no-cache-dir --upgrade pip

# Salin requirements.txt
COPY requirements.txt .

# Instal dependensi. Langkah ini akan jauh lebih cepat sekarang.
RUN pip install --no-cache-dir -r requirements.txt


# Tahap 2: "Runner" - Kita tetap pakai -slim di sini untuk image akhir yang kecil.
FROM python:3.11-slim

WORKDIR /app

# Salin HANYA virtual environment yang sudah jadi dari tahap builder.
COPY --from=builder /opt/venv /opt/venv

# Atur PATH untuk menggunakan venv
ENV PATH="/opt/venv/bin:$PATH"

# Salin kode aplikasi dan data
# Pastikan tidak ada file besar yang tidak perlu di sini.
COPY ./app ./app
COPY ./data ./data
COPY ./chroma_db ./chroma_db
COPY ./tests ./tests

# Ekspos port
EXPOSE 8000

# Jalankan aplikasi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]