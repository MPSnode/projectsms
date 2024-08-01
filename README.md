```markdown
# Bulk SMS Sender

## Deskripsi
Script ini memungkinkan Anda mengirim SMS massal menggunakan modem GSM atau ponsel yang terhubung ke komputer melalui USB. Script ini mendeteksi perangkat, memeriksa koneksi, dan mengirim SMS ke nomor target.

## Prerequisites
Sebelum menjalankan script ini, pastikan Anda telah memenuhi persyaratan berikut:

1. **Python 3.12** atau versi terbaru terinstal di komputer Anda.
2. Modem GSM atau ponsel yang terhubung melalui USB.
3. Driver yang diperlukan untuk modem GSM atau ponsel terinstal dengan benar.

## Instalasi
1. **Clone repository**:
   ```bash
   git clone https://github.com/username/repository.git
   cd repository
   ```

2. **Instal dependensi**:
   Pastikan Anda telah menginstal `pip`. Kemudian, instal semua dependensi yang diperlukan dengan perintah:
   ```bash
   pip install -r requirements.txt
   ```

## Menyiapkan Data
1. **File Modem dan Ponsel**:
   - Buat file `data/modems.txt` yang berisi daftar port serial modem atau ponsel yang terhubung, satu per baris. Contoh:
     ```
     /dev/ttyUSB0
     /dev/ttyUSB1
     ```

2. **File Pesan dan Nomor Telepon**:
   - Buat file `data/messages.txt` untuk menyimpan pesan-pesan yang akan dikirim.
   - Buat file `data/numbers.txt` untuk menyimpan nomor-nomor telepon target.

## Menjalankan Script
1. **Jalankan Script**:
   Untuk menjalankan script, gunakan perintah berikut:
   ```bash
   python send_sms.py
   ```

2. **Interaksi dengan Script**:
   - Script akan meminta Anda memilih jenis perangkat yang digunakan (Modem GSM atau Ponsel).
   - Setelah memilih perangkat, script akan mendeteksi port USB yang terhubung dan memeriksa koneksi.
   - Anda akan diberikan opsi untuk mengatur pesan, nomor telepon, dan memulai pengiriman SMS.
   - Anda dapat memilih untuk menggunakan satu modem/ponsel atau semua modem/ponsel yang terhubung.

## Catatan
- Pastikan perangkat modem GSM atau ponsel terhubung dan dikenali oleh sistem operasi Anda.
- Jika perangkat tidak terdeteksi, pastikan driver terinstal dengan benar dan perangkat terhubung ke port yang benar.

## Troubleshooting
- **Perangkat Tidak Terhubung**: Pastikan perangkat terhubung dengan benar dan port serial yang digunakan sesuai.
- **Tidak Ada Respons**: Periksa kabel USB dan driver perangkat.
- **Pesan Tidak Terkirim**: Verifikasi bahwa saldo pulsa mencukupi dan nomor tujuan valid.

## Kontribusi
Jika Anda menemukan bug atau memiliki fitur tambahan yang diinginkan, silakan buka issue di GitHub repository ini atau kirim pull request.

## Lisensi
Script ini dilisensikan di bawah [Lisensi MIT](LICENSE).

## BY MPS1310
```

CONTACT INFORMASION
-EMAIL:
-TELEGRAM:
