import serial
import serial.tools.list_ports
import time
from colorama import init, Fore

# Inisialisasi colorama
init(autoreset=True)

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
    # Tampilkan daftar port serial
    list_serial_ports()

    devices = read_lines('data/modems.txt')

    if not devices:
        print(Fore.RED + "Daftar perangkat kosong atau tidak ditemukan.")
        return

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
                for device_port in devices:
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
                        print(Fore.YELLOW + "[2] ALL MODEM")

                        method_choice = input("Pilih metode: ").strip()
                        
                        if method_choice == '1':
                            print(Fore.YELLOW + "SELECT THE MODEM YOU WANT TO USE:")
                            for index, modem in enumerate(modems_initialized):
                                print(Fore.YELLOW + f"[{index+1}] MODEM {index+1}")

                            modem_choice = int(input("Pilih modem: ").strip()) - 1
                            if 0 <= modem_choice < len(modems_initialized):
                                selected_modem = modems_initialized[modem_choice]
                                print(Fore.GREEN + f"Selected MODEM: {selected_modem.port}")
                                for phone_number in phone_numbers:
                                    for message in messages:
                                        status, error = selected_modem.send_sms(phone_number, message)
                                        print(Fore.CYAN + f"MODEM: {selected_modem.port}")
                                        print(Fore.CYAN + f"NUMBER: {phone_number}")
                                        print(status)
                                        if error:
                                            print(error)
                                selected_modem.close()
                            else:
                                print(Fore.RED + "Pilihan modem tidak valid.")
                        
                        elif method_choice == '2':
                            for modem in modems_initialized:
                                print(Fore.GREEN + f"Processing with MODEM: {modem.port}")
                                for phone_number in phone_numbers:
                                    for message in messages:
                                        status, error = modem.send_sms(phone_number, message)
                                        print(Fore.CYAN + f"MODEM: {modem.port}")
                                        print(Fore.CYAN + f"NUMBER: {phone_number}")
                                        print(status)
                                        if error:
                                            print(error)
                                modem.close()
                        
                        else:
                            print(Fore.RED + "Metode tidak valid.")

                        break
                    else:
                        print(Fore.RED + "Pilihan tidak valid.")

            elif device_choice == '2':
                # Deteksi ponsel
                phones_initialized = []
                for device_port in devices:
                    if detect_device(device_port):
                        phone = MobilePhone(device_port)
                        if phone.initialize():
                            phones_initialized.append(phone)
                        else:
                            print(Fore.RED + f"LOGIN FAILURE!! {device_port}")
                    else:
                        print(Fore.RED + f"PLEASE CONNECT USB FIRST: {device_port}")

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
                            print(Fore.YELLOW + "SELECT THE PHONE YOU WANT TO USE:")
                            for index, phone in enumerate(phones_initialized):
                                print(Fore.YELLOW + f"[{index+1}] PHONE {index+1}")

                            phone_choice = int(input("Pilih ponsel: ").strip()) - 1
                            if 0 <= phone_choice < len(phones_initialized):
                                selected_phone = phones_initialized[phone_choice]
                                print(Fore.GREEN + f"Selected PHONE: {selected_phone.port}")
                                for phone_number in phone_numbers:
                                    for message in messages:
                                        status, error = selected_phone.send_sms(phone_number, message)
                                        print(Fore.CYAN + f"PHONE: {selected_phone.port}")
                                        print(Fore.CYAN + f"NUMBER: {phone_number}")
                                        print(status)
                                        if error:
                                            print(error)
                                selected_phone.close()
                            else:
                                print(Fore.RED + "Pilihan ponsel tidak valid.")
                        
                        elif method_choice == '2':
                            for phone in phones_initialized:
                                print(Fore.GREEN + f"Processing with PHONE: {phone.port}")
                                for phone_number in phone_numbers:
                                    for message in messages:
                                        status, error = phone.send_sms(phone_number, message)
                                        print(Fore.CYAN + f"PHONE: {phone.port}")
                                        print(Fore.CYAN + f"NUMBER: {phone_number}")
                                        print(status)
                                        if error:
                                            print(error)
                                phone.close()
                        
                        else:
                            print(Fore.RED + "Metode tidak valid.")

                        break
                    else:
                        print(Fore.RED + "Pilihan tidak valid.")

        else:
            print(Fore.RED + "Pilihan perangkat tidak valid.")

if __name__ == "__main__":
    main()
