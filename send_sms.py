import os
import sys
import hashlib
import serial
import serial.tools.list_ports
import time
from colorama import init, Fore

# Inisialisasi colorama
init(autoreset=True)

def load_access_key_hash(file_path):
    """ Membaca hash kunci akses dari file biner """
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} tidak ditemukan.")
        sys.exit(1)

def check_access_key():
    """ Memeriksa akses key yang dimasukkan pengguna """
    access_key_file = 'path/to/access_key.bin'  # Ganti dengan path yang sesuai
    valid_access_key_hash = load_access_key_hash(access_key_file)
    
    user_input = input("Masukkan kode akses: ").strip()
    user_input_hash = hashlib.md5(user_input.encode()).digest()
    
    if user_input_hash == valid_access_key_hash:
        print(Fore.GREEN + "Akses berhasil!")
        return True
    else:
        print(Fore.RED + "Kode akses tidak valid.")
        sys.exit(1)

def list_serial_ports():
    """ Mencetak daftar port serial yang tersedia """
    print(Fore.YELLOW + "\nDaftar port serial yang tersedia:")
    ports = serial.tools.list_ports.comports()
    if ports:
        for port in ports:
            print(Fore.GREEN + f"Port: {port.device} - {port.description}")
    else:
        print(Fore.RED + "Tidak ada port serial yang ditemukan.")

def detect_device(device_port):
    """ Mendeteksi apakah perangkat terhubung dan dapat diakses """
    try:
        print(Fore.YELLOW + f"Memeriksa {device_port}...")
        with serial.Serial(device_port, timeout=1) as ser:
            ser.write(b'AT\r')
            time.sleep(1)
            response = ser.read(100)
            print(Fore.CYAN + f"Respons dari {device_port}: {response.decode(errors='ignore')}")
            if b'OK' in response:
                print(Fore.GREEN + f"Device detected at {device_port}.")
                return True
            else:
                print(Fore.RED + f"Device not responding properly at {device_port}.")
                return False
    except (serial.SerialException, FileNotFoundError) as e:
        print(Fore.RED + f"Error accessing {device_port}: {e}")
        return False

def read_lines(file_path):
    """ Membaca baris dari file """
    try:
        with open(file_path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
        print(Fore.GREEN + f"Read {len(lines)} lines from {file_path}.")
        return lines
    except FileNotFoundError:
        print(Fore.RED + f"File {file_path} tidak ditemukan.")
        return []

def write_lines(file_path, lines):
    """ Menulis baris ke file """
    try:
        with open(file_path, 'w') as file:
            for line in lines:
                file.write(line + '\n')
        print(Fore.GREEN + f"Successfully wrote {len(lines)} lines to {file_path}.")
    except Exception as e:
        print(Fore.RED + f"Error writing to {file_path}: {e}")

class GSMModem:
    def __init__(self, port):
        self.port = port
        self.serial = None

    def initialize(self):
        """ Menginisialisasi modem """
        try:
            self.serial = serial.Serial(self.port, baudrate=9600, timeout=5)
            self.serial.write(b'AT\r')
            time.sleep(1)
            response = self.serial.read(100)
            print(Fore.CYAN + f"Respons dari {self.port}: {response.decode(errors='ignore')}")
            if b'OK' in response:
                print(Fore.GREEN + f"SUCCESSFUL LOGIN!!! ({self.port})")
                return True
            else:
                print(Fore.RED + f"LOGIN FAILURE!! ({self.port})")
                return False
        except serial.SerialException as e:
            print(Fore.RED + f"Error initializing modem at {self.port}: {e}")
            return False

    def send_sms(self, phone_number, message):
        """ Mengirim SMS menggunakan modem """
        try:
            self.serial.write(b'AT+CMGF=1\r')  # Set SMS to text mode
            time.sleep(1)
            self.serial.write(f'AT+CMGS="{phone_number}"\r'.encode())
            time.sleep(1)
            self.serial.write((message + chr(26)).encode())  # 26 is the ASCII code for Ctrl+Z
            time.sleep(1)
            response = self.serial.read(100)
            print(Fore.CYAN + f"Respons dari {self.port}: {response.decode(errors='ignore')}")
            if b'OK' in response:
                return Fore.GREEN + "INFO: SENDING SUCCESS!!", None
            else:
                return Fore.RED + "INFO: SEND FAILURE!!", Fore.RED + "KET: ERROR"
        except serial.SerialException as e:
            return Fore.RED + "INFO: SEND FAILURE!!", Fore.RED + f"KET: {e}"

    def close(self):
        """ Menutup koneksi modem """
        if self.serial:
            self.serial.close()
            print(Fore.YELLOW + f"Modem at {self.port} closed.")

class MobilePhone:
    def __init__(self, port):
        self.port = port
        self.serial = None

    def initialize(self):
        """ Menginisialisasi ponsel """
        try:
            self.serial = serial.Serial(self.port, baudrate=9600, timeout=5)
            self.serial.write(b'AT\r')
            time.sleep(1)
            response = self.serial.read(100)
            print(Fore.CYAN + f"Respons dari {self.port}: {response.decode(errors='ignore')}")
            if b'OK' in response:
                print(Fore.GREEN + f"SUCCESSFUL LOGIN!!! ({self.port})")
                return True
            else:
                print(Fore.RED + f"LOGIN FAILURE!! ({self.port})")
                return False
        except serial.SerialException as e:
            print(Fore.RED + f"Error initializing phone at {self.port}: {e}")
            return False

    def send_sms(self, phone_number, message):
        """ Mengirim SMS menggunakan ponsel """
        try:
            self.serial.write(b'AT+CMGF=1\r')  # Set SMS to text mode
            time.sleep(1)
            self.serial.write(f'AT+CMGS="{phone_number}"\r'.encode())
            time.sleep(1)
            self.serial.write((message + chr(26)).encode())  # 26 is the ASCII code for Ctrl+Z
            time.sleep(1)
            response = self.serial.read(100)
            print(Fore.CYAN + f"Respons dari {self.port}: {response.decode(errors='ignore')}")
            if b'OK' in response:
                return Fore.GREEN + "INFO: SENDING SUCCESS!!", None
            else:
                return Fore.RED + "INFO: SEND FAILURE!!", Fore.RED + "KET: ERROR"
        except serial.SerialException as e:
            return Fore.RED + "INFO: SEND FAILURE!!", Fore.RED + f"KET: {e}"

    def close(self):
        """ Menutup koneksi ponsel """
        if self.serial:
            self.serial.close()
            print(Fore.YELLOW + f"Phone at {self.port} closed.")

def main():
    # Memeriksa akses key
    if not check_access_key():
        return

    # Tampilkan daftar port serial
    list_serial_ports()

    modems = read_lines('data/modems.txt')
    phones = read_lines('data/phones.txt')

    if not modems:
        print(Fore.RED + "Daftar modem kosong atau tidak ditemukan.")
    
    if not phones:
        print(Fore.RED + "Daftar ponsel kosong atau tidak ditemukan.")
    
    while True:
        print(Fore.YELLOW + "\n[1] Gunakan Modem GSM")
        print(Fore.YELLOW + "[2] Gunakan Ponsel")
        device_choice = input("Pilih perangkat: ").strip()

        if device_choice in ['1', '2']:
            # Mulai proses deteksi perangkat
            print(Fore.YELLOW + "Loading...")
            time.sleep(2)  # Simulasi loading
            
            if device_choice == '1':
                # Deteksi modem
                modems_initialized = []
                for device_port in modems:
                    if detect_device(device_port):
                        modem = GSMModem(device_port)
                        if modem.initialize():
                            modems_initialized.append(modem)
                        else:
                            print(Fore.RED + f"LOGIN FAILURE!! {device_port}")
                    else:
                        print(Fore.RED + f"PLEASE CONNECT USB FIRST: {device_port}")

                if not modems_initialized:
                    print(Fore.RED + "Tidak ada modem yang berhasil diinisialisasi.")
                    return

                # Menampilkan info perangkat
                print(Fore.CYAN + "\nINFO:")
                print(Fore.CYAN + "____________________________________")
                for i, modem in enumerate(modems_initialized):
                    print(Fore.CYAN + f"MODEM {i+1}: {modem.port}")
                print(Fore.CYAN + "PROVIDER: GSM Modem")
                print(Fore.CYAN + "____________________________________")

                while True:
                    print(Fore.YELLOW + "\n[1] SET MESSAGE")
                    print(Fore.YELLOW + "[2] SET NUMBER")
                    print(Fore.YELLOW + "[3] START")

                    choice = input("Pilih opsi: ").strip()

                    if choice == '1':
                        print(Fore.YELLOW + "Memilih pesan...")
                        # Update pesan jika diperlukan
                    elif choice == '2':
                        print(Fore.YELLOW + "Memilih nomor telepon...")
                        # Update nomor telepon jika diperlukan
                    elif choice == '3':
                        print(Fore.YELLOW + "CHOOSE THE METHOD YOU WANT TO USE:")
                        print(Fore.YELLOW + "[1] SINGLE MODEM")
                        print(Fore.YELLOW + "[2] ALL MODEMS")

                        method_choice = input("Pilih metode: ").strip()

                        if method_choice == '1':
                            phone_numbers = read_lines('data/nomor.txt')
                            message = 'Insert your message here'  # Ganti dengan pesan yang diinginkan

                            print(Fore.YELLOW + "Pilih modem yang akan digunakan:")
                            for i, modem in enumerate(modems_initialized):
                                print(Fore.YELLOW + f"[{i + 1}] {modem.port}")

                            modem_index = int(input("Masukkan nomor modem: ").strip()) - 1

                            if 0 <= modem_index < len(modems_initialized):
                                selected_modem = modems_initialized[modem_index]
                                for phone_number in phone_numbers:
                                    status, error_message = selected_modem.send_sms(phone_number, message)
                                    if status:
                                        print(Fore.GREEN + f"Nomor: {phone_number} - {status}")
                                    if error_message:
                                        print(Fore.RED + f"Nomor: {phone_number} - {error_message}")

                                selected_modem.close()
                                break
                            else:
                                print(Fore.RED + "Nomor modem tidak valid.")
                        elif method_choice == '2':
                            phone_numbers = read_lines('data/nomor.txt')
                            message = 'Insert your message here'  # Ganti dengan pesan yang diinginkan

                            for phone_number in phone_numbers:
                                for modem in modems_initialized:
                                    status, error_message = modem.send_sms(phone_number, message)
                                    if status:
                                        print(Fore.GREEN + f"Nomor: {phone_number} - {status}")
                                    if error_message:
                                        print(Fore.RED + f"Nomor: {phone_number} - {error_message}")

                            for modem in modems_initialized:
                                modem.close()
                            break
                        else:
                            print(Fore.RED + "Pilihan metode tidak valid.")
                    else:
                        print(Fore.RED + "Pilihan tidak valid.")
            elif device_choice == '2':
                # Deteksi ponsel
                detected_phones = []
                print(Fore.YELLOW + "Mendeteksi ponsel yang terhubung...")
                ports = serial.tools.list_ports.comports()
                for port in ports:
                    if detect_device(port.device):
                        detected_phones.append(port.device)

                if detected_phones:
                    write_lines('data/phones.txt', detected_phones)
                    print(Fore.GREEN + "Informasi port ponsel berhasil disimpan.")
                else:
                    print(Fore.RED + "Tidak ada ponsel yang terdeteksi.")

                phones_initialized = []
                for device_port in detected_phones:
                    phone = MobilePhone(device_port)
                    if phone.initialize():
                        phones_initialized.append(phone)
                    else:
                        print(Fore.RED + f"LOGIN FAILURE!! {device_port}")

                if not phones_initialized:
                    print(Fore.RED + "Tidak ada ponsel yang berhasil diinisialisasi.")
                    return

                # Menampilkan info perangkat
                print(Fore.CYAN + "\nINFO:")
                print(Fore.CYAN + "____________________________________")
                for i, phone in enumerate(phones_initialized):
                    print(Fore.CYAN + f"PHONE {i+1}: {phone.port}")
                print(Fore.CYAN + "PROVIDER: Mobile Phone")
                print(Fore.CYAN + "____________________________________")

                while True:
                    print(Fore.YELLOW + "\n[1] SET MESSAGE")
                    print(Fore.YELLOW + "[2] SET NUMBER")
                    print(Fore.YELLOW + "[3] START")

                    choice = input("Pilih opsi: ").strip()

                    if choice == '1':
                        print(Fore.YELLOW + "Memilih pesan...")
                        # Update pesan jika diperlukan
                    elif choice == '2':
                        print(Fore.YELLOW + "Memilih nomor telepon...")
                        # Update nomor telepon jika diperlukan
                    elif choice == '3':
                        print(Fore.YELLOW + "CHOOSE THE METHOD YOU WANT TO USE:")
                        print(Fore.YELLOW + "[1] SINGLE PHONE")
                        print(Fore.YELLOW + "[2] ALL PHONES")

                        method_choice = input("Pilih metode: ").strip()

                        if method_choice == '1':
                            phone_numbers = read_lines('data/nomor.txt')
                            message = 'Insert your message here'  # Ganti dengan pesan yang diinginkan

                            print(Fore.YELLOW + "Pilih ponsel yang akan digunakan:")
                            for i, phone in enumerate(phones_initialized):
                                print(Fore.YELLOW + f"[{i + 1}] {phone.port}")

                            phone_index = int(input("Masukkan nomor ponsel: ").strip()) - 1

                            if 0 <= phone_index < len(phones_initialized):
                                selected_phone = phones_initialized[phone_index]
                                for phone_number in phone_numbers:
                                    status, error_message = selected_phone.send_sms(phone_number, message)
                                    if status:
                                        print(Fore.GREEN + f"Nomor: {phone_number} - {status}")
                                    if error_message:
                                        print(Fore.RED + f"Nomor: {phone_number} - {error_message}")

                                selected_phone.close()
                                break
                            else:
                                print(Fore.RED + "Nomor ponsel tidak valid.")
                        elif method_choice == '2':
                            phone_numbers = read_lines('data/nomor.txt')
                            message = 'Insert your message here'  # Ganti dengan pesan yang diinginkan

                            for phone_number in phone_numbers:
                                for phone in phones_initialized:
                                    status, error_message = phone.send_sms(phone_number, message)
                                    if status:
                                        print(Fore.GREEN + f"Nomor: {phone_number} - {status}")
                                    if error_message:
                                        print(Fore.RED + f"Nomor: {phone_number} - {error_message}")

                            for phone in phones_initialized:
                                phone.close()
                            break
                        else:
                            print(Fore.RED + "Pilihan metode tidak valid.")
                    else:
                        print(Fore.RED + "Pilihan tidak valid.")
        else:
            print(Fore.RED + "Pilihan perangkat tidak valid.")
            return

if __name__ == "__main__":
    main()
