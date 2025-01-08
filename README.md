Step by Step

Create environment
1. python -m venv nama_environment
2. env\Scripts\Activate.bat
3. cd penjualan_kerudung
4. python manage.py runserver

Jika tidak ada database sebelumnya bisa lakukan
1. python manage.py makemigrations
2. python manage.py migrate
3. python manage.py createsuperuser
4. Tambahkan username contoh admin
5. Tambahkan email contoh admin@gmail.com
6. Tambahkan password contoh admin
7. Tambahkan password again yang sama
8. Ketik y
9. Lalu jalankan python manage.py runserver
