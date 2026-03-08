# tests/test_main.py

from fastapi.testclient import TestClient
from app.main import app  # Impor objek 'app' utama dari paket aplikasi Anda

# Buat sebuah klien tes yang akan berinteraksi dengan aplikasi kita
client = TestClient(app)

def test_read_root():
    """
    Tes untuk memastikan endpoint root ("/") berfungsi dan mengembalikan pesan selamat datang.
    """
    # Lakukan permintaan GET ke path "/"
    response = client.get("/")

    # Periksa apakah responsnya sukses (status code 200)
    assert response.status_code == 200

    # Periksa apakah isi JSON dari respons sesuai dengan yang diharapkan
    assert response.json() == {"message": "Selamat datang! Silakan kunjungi /docs untuk melihat endpoint yang tersedia."}


def test_ask_rag_endpoint_success():
    """
    Tes untuk kasus sukses pada endpoint POST /rag/ask.
    Kita akan menguji dengan pertanyaan yang kita tahu ada di dalam database Chroma kita.
    """
    # Siapkan data permintaan (request body)
    request_data = {"question": "Kapan Go-Jek memulai layanannya?"}

    # Lakukan permintaan POST ke endpoint /rag/ask
    response = client.post("/rag/ask", json=request_data)

    # Periksa apakah responsnya sukses
    assert response.status_code == 200

    # Dapatkan data JSON dari respons
    response_data = response.json()

    # Periksa apakah respons memiliki kunci 'answer' yang kita harapkan
    assert "answer" in response_data

    # Periksa apakah jawaban yang diberikan mengandung kata kunci yang diharapkan (misal, "2010")
    # Ini adalah cara sederhana untuk memverifikasi kebenaran jawaban tanpa harus sama persis.
    assert "2010" in response_data["answer"]


def test_ask_rag_endpoint_not_found():
    """
    Tes untuk kasus di mana informasi tidak ada di database.
    Kita mengharapkan jawaban yang sopan bahwa data tidak ditemukan.
    """
    # Siapkan data permintaan dengan pertanyaan yang tidak relevan
    request_data = {"question": "Apa ibu kota Mars?"}

    # Lakukan permintaan POST
    response = client.post("/rag/ask", json=request_data)

    # Periksa apakah responsnya tetap sukses (karena secara teknis API tidak error)
    assert response.status_code == 200

    # Dapatkan data JSON dari respons
    response_data = response.json()

    # Periksa apakah kunci 'answer' ada
    assert "answer" in response_data

    # Periksa apakah jawaban yang diberikan adalah pesan "tidak ditemukan" yang kita program di prompt
    assert "tidak dapat menemukan informasi" in response_data["answer"]