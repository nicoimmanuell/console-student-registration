from logging import exception
import mysql.connector
import os

database = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="dbmahasiswa",
    autocommit=True
)

cursor = database.cursor(buffered = True)

class Mahasiswa:

    def __init__(self, nim, nama, prodi, jenis_kelamin, angkatan, alamat, no_telp, biaya_kuliah):
        self.nim = nim
        self.name = nama
        self.prodi = prodi
        self.jenis_kelamin = jenis_kelamin
        self.angkatan = angkatan
        self.alamat = alamat
        self.no_telp = no_telp
        self.biaya_kuliah = biaya_kuliah
    
    @staticmethod
    def tambah_mhs():
        clear()
        gender_list = ["Wanita", "Pria"]
        nim = input("Masukkan NIM : ")
        nama = input("Masukkan nama mahasiswa : ")
        cursor.execute("SELECT Nama FROM prodi")
        result = cursor.fetchall()
        while(True):
            clear()
            i =1
            for prodi in result:
                prodi = prodi[0]
                print("{}.".format(i), prodi)
                i = i + 1
            try:
                prodi = result[int(input("Masukkan nomor program studi: "))-1][0]
                break
            except:
                print("Error, anda mungkin memasukkan angka yang salah atau huruf")
        while(True):
            i =1
            for gender in gender_list:
                print("{}.".format(i), gender)
                i = i + 1
            try:
                gender = gender_list[int(input("Masukkan gender : "))-1]
                break
            except:
                print("Error, anda mungkin memasukkan angka yang salah atau huruf")
        angkatan = input("Masukkan angkatan mahasiswa : ")
        alamat = input("Masukkan alamat mahasiswa : ")
        no_telp = input("Masukkan nomor telepon mahasiswa : ")
        cursor.execute("SELECT BiayaUKT FROM prodi WHERE Nama = '{}'".format(prodi))
        biaya = cursor.fetchone()[0]
        while True:
            save_data = input("Simpan data mahasiswa? (Y/N) ")
            save = save_data.upper()
            if (save == "Y"):
                temp_mhs = Mahasiswa(nim, nama, prodi, gender, angkatan, alamat, no_telp, biaya)
                sql = "INSERT INTO mahasiswa (NIM, Nama, ProgramStudi, JenisKelamin, Angkatan, Alamat, NomorTelepon, BiayaKuliah) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                val = (temp_mhs.nim, temp_mhs.name, temp_mhs.prodi, temp_mhs.jenis_kelamin, temp_mhs.angkatan, temp_mhs.alamat, temp_mhs.no_telp, temp_mhs.biaya_kuliah)
                try:
                    cursor.execute(sql, val)
                    input("\nData tersimpan! Tekan enter untuk kembali..")
                    break
                except:
                    print("\nTerjadi kesalahan input atau NIM sudah terdaftar")
                    input("Harap coba masukkan data lagi")
            elif(save =="N"):
                input("Data tidak tersimpan! Tekan enter untuk kembali..")
                break
            else:
                print("\nInput tidak valid")
                input("Tekan enter untuk melanjutkan..")
    
    @staticmethod
    def sort_mhs_by(data):
        cursor.execute("SELECT * FROM mahasiswa ORDER BY {} ASC".format(data))


    @staticmethod
    def show_mhs():
        cursor.execute("SELECT * FROM mahasiswa")
        while True:
            clear()
            option = ['Nama', 'Urutkan berdasarkan NIM', 'Kembali']
            attr = ['NIM', 'Nama', 'Program Studi', 'Jenis Kelamin', 'Angkatan', 'Alamat', 'Nomor Telepon', 'Biaya Kuliah']
            result = cursor.fetchall()
            num= 0
            print("-"*196)
            print(
                f"| {'No': <4} | {attr[0]:<10} | {attr[1]: <30} | {attr[2]: <25} | {attr[3]: <20} | {attr[4]: <15} | {attr[5]: <20} | {attr[6]: <20} | {attr[7]: <24} |")
            print("-"*196)
            for result in result:
                print(
                    f"| {num+1:<4} | {str(result[0]):<10} | {result[1]:<30} | {result[2]:<25} | {result[3]:<20} | {str(result[4]):<15} | {result[5]:<20} | {result[6]:<20} | Rp. {str(result[7]):<20} |")
                num +=1
            print("-"*196)
            option_num = 1
            print("Urutkan berdasarkan : ")
            for data in option:
                print(option_num, ". ", data)
                option_num +=1 
            pick = int(input("Masukkan pilihan : "))
            if (pick == 1):
                clear()
                Mahasiswa.sort_mhs_by(attr[1])
            if (pick == 2):
                clear()
                Mahasiswa.sort_mhs_by(attr[0])
            if (pick == 3):
                break
    

                

    @staticmethod
    def find_mhs(code):
        def confirm(code, sql, val):
            if code != "":
                verify = input("Masukkan kode akses untuk melanjutkan : ")
                if verify == code:
                    cursor.execute(sql, val)
                    print("Kode akses diterima, data diubah")
                else:
                    print("Kode akses salah, data tidak diubah")
            else:
                cursor.execute(sql, val)

        def change_mhs(res, code):
            menu = ['Ubah Nama','Ubah Prodi','Ubah Alamat', 'Hapus Data','Kembali']
            while True:
                num = 0
                no = 0
                for i in range(len(menu)):
                    print(i+1,". ", menu[i])
                choose = input("Masukkan pilihan anda : ")
                if choose == "1":
                    clear()
                    new_name = input("Masukkan nama baru : ")
                    sql = "UPDATE mahasiswa SET Nama = %s WHERE NIM = %s"
                    val = (new_name, res)
                    confirm(code, sql, val)
                    cursor.execute("SELECT * FROM mahasiswa WHERE NIM = {}".format(res))
                    result = cursor.fetchall()
                    print("-"*196)
                    print(
                        f"| {'No': <4} | {attr[0]:<10} | {attr[1]: <30} | {attr[2]: <25} | {attr[3]: <20} | {attr[4]: <15} | {attr[5]: <20} | {attr[6]: <20} | {attr[7]: <24} |")
                    print("-"*196)
                    for result in result:
                        print(
                        f"| {no+1 : <4} | {result[0]:<10} | {result[1]: <30} | {result[2]: <25} | {result[3]: <20} | {result[4]: <15} | {result[5]: <20} | {result[6]: <20} | Rp. {result[7]: <20} |")
                        no += 1
                    print("-"*196)
                
                if choose == "2":
                    clear()
                    cursor.execute("SELECT Nama FROM prodi")
                    rest = cursor.fetchall()
                    num = 0
                    no = 0
                    for prod in rest:
                        print(num+1,'. ', prod[0])
                        num+=1
                    pick = int(input("Masukkan nomor pilihan anda : "))
                    prodi = rest[pick-1][0]
                    sql = "UPDATE mahasiswa SET ProgramStudi = %s WHERE NIM = %s"
                    val = (prodi, res)
                    confirm(code, sql, val)
                    cursor.execute("SELECT * FROM mahasiswa WHERE NIM = {}".format(res))
                    result = cursor.fetchall()
                    clear()
                    print("-"*196)
                    print(
                        f"| {'No': <4} | {attr[0]:<10} | {attr[1]: <30} | {attr[2]: <25} | {attr[3]: <20} | {attr[4]: <15} | {attr[5]: <20} | {attr[6]: <20} | {attr[7]: <24} |")
                    print("-"*196)
                    for result in result:
                        print(
                        f"| {no+1 : <4} | {result[0]:<10} | {result[1]: <30} | {result[2]: <25} | {result[3]: <20} | {result[4]: <15} | {result[5]: <20} | {result[6]: <20} | Rp. {result[7]: <20} |")
                        no += 1
                    print("-"*196)
                                
                if choose == "3":
                    clear()
                    new_addrs = input("Masukkan alamat baru : ")
                    sql = "UPDATE mahasiswa SET Alamat = %s WHERE NIM = %s"
                    val = (new_addrs, res)
                    confirm(code, sql, val)
                    cursor.execute("SELECT * FROM mahasiswa WHERE NIM = {}".format(res))
                    result = cursor.fetchall()
                    clear()
                    print("-"*196)
                    print(
                        f"| {'No': <4} | {attr[0]:<10} | {attr[1]: <30} | {attr[2]: <25} | {attr[3]: <20} | {attr[4]: <15} | {attr[5]: <20} | {attr[6]: <20} | {attr[7]: <24} |")
                    print("-"*196)
                    for result in result:
                        print(
                        f"| {no+1 : <4} | {result[0]:<10} | {result[1]: <30} | {result[2]: <25} | {result[3]: <20} | {result[4]: <15} | {result[5]: <20} | {result[6]: <20} | Rp. {result[7]: <20} |")
                        no += 1
                    print("-"*196)
                if choose == "4":
                    clear()
                    sql = "DELETE FROM mahasiswa WHERE NIM = %s"
                    verify = input("Masukkan kode akses untuk melanjutkan : ")
                    if code != "":
                        if verify == code:
                            cursor.execute(sql, (res,))
                            print("Kode akses diterima, data dihapus")
                            input("Tekan enter untuk melanjutkan...")
                        else:
                            print("Kode akses salah, data tidak dihapus")
                    else:
                        cursor.execute(sql, (res,))
                
                if choose == "5":
                    break
                
                    

        def query_result(result, choose, code):
            num = 0
            if cursor.rowcount != 0:
                print("-"*196)
                print(
                    f"| {'No': <4} | {attr[0]:<10} | {attr[1]: <30} | {attr[2]: <25} | {attr[3]: <20} | {attr[4]: <15} | {attr[5]: <20} | {attr[6]: <20} | {attr[7]: <24} |")
                print("-"*196)
                for result in result:
                    print(
                    f"| {num+1 : <4} | {result[0]:<10} | {result[1]: <30} | {result[2]: <25} | {result[3]: <20} | {result[4]: <15} | {result[5]: <20} | {result[6]: <20} | Rp. {result[7]: <20} |")
                    num += 1
                print("-"*196)
                if choose < 3 and cursor.rowcount == 1:
                        change_mhs(result[0], code)
                else:
                    input('Tekan enter untuk kembali...')
            else:
                print('Mahasiswa tidak ditemukan')
                input('Tekan enter untuk kembali...')
        while True:
            clear()
            option = ['NIM', 'Nama', 'Program Studi', 'Angkatan', 'Kembali']
            attr = ['NIM', 'Nama', 'Program Studi', 'Jenis Kelamin', 'Angkatan', 'Alamat', 'Nomor Telepon', 'Biaya Kuliah']
            num = 0
            print('Cari mahasiswa berdasarkan : \n')
            for option in option:
                print(num+1,". ", option)
                num += 1
            try:
                choose = int(input('\nMasukkan pilihan anda : '))
            except:
                print("Harap masukkan angka")
                input("Tekan enter untuk melanjutkan...")
            if choose > 0 and choose < 6:
                if (choose == 1):
                    clear()
                    value = int(input("Masukkan NIM yang ingin dicari : "))
                    cursor.execute("SELECT * FROM mahasiswa WHERE NIM = {}".format(value))
                    result = cursor.fetchall()
                    query_result(result, choose, code)
                if (choose == 2):
                    clear()
                    value = input("Masukkan nama mahasiswa yang ingin dicari : ")
                    cursor.execute("SELECT * FROM mahasiswa WHERE Nama = '{}'".format(value))
                    result = cursor.fetchall()
                    query_result(result, choose, code)
                if (choose == 3):
                    clear()
                    value = input("Masukkan nama program studi yang ingin dicari : ")
                    cursor.execute("SELECT * FROM mahasiswa WHERE ProgramStudi = '{}'".format(value))
                    result = cursor.fetchall()
                    query_result(result, choose, code)
                if (choose == 4):
                    clear()
                    value = input("Masukkan angkatan yang ingin dicari : ")
                    cursor.execute("SELECT * FROM mahasiswa WHERE Angkatan = {}".format(value))
                    result = cursor.fetchall()
                    query_result(result, choose, code)
                if (choose == 5):
                    break


class Prodi:

    def __init__(self, id, nama, akreditasi, ukt):
        self.id = id
        self.nama = nama
        self.akreditasi = akreditasi
        self.ukt = ukt
    
    @staticmethod
    def tambah_prodi():
        clear()
        id = input("Masukkan ID Prodi : ")
        nama = input("Masukkan nama program studi : ")
        akreditasi = input("Masukkan nama akreditasi : ")
        ukt = int(input("Masukkan biaya UKT program studi : "))
        temp_prodi = Prodi(id, nama, akreditasi, ukt)
        
        sql = "INSERT INTO prodi (ID, Nama, Akreditasi, BiayaUKT) VALUES (%s, %s, %s, %s)"
        val = (temp_prodi.id, temp_prodi.nama, temp_prodi.akreditasi, temp_prodi.ukt)
        cursor.execute(sql, val)
        return temp_prodi

    @staticmethod
    def sort_prodi_by(data):
        cursor.execute("SELECT * FROM prodi ORDER BY {} ASC".format(data))
    
    @staticmethod
    def show_prodi():
        cursor.execute("SELECT * FROM prodi")
        while True:
            clear()
            option = ['Urutkan berdasarkan nama prodi', 'Urutkan berdasarkan ID', 'Urutkan berdasarkan biaya UKT', 'Kembali']
            attr = ['ID', 'Nama', 'Akreditasi', 'BiayaUKT']
            result = cursor.fetchall()
            num= 0
            print("-"*99)
            print(
                f"| {'No': <4} | {'ID': <15} | {'Nama':<30} | {'Akreditasi': <15} | {'Biaya UKT': <19} |")
            print("-"*99)
            for result in result:
                print(
                    f"| {num+1:<4} | {str(result[0]):<15} | {result[1]:<30} | {result[2]:<15} | Rp. {result[3]: <15} |")
                num +=1
            print("-"*99)
            option_num = 1
            print("Pilih Opsi : ")
            for data in option:
                print(option_num, ". ", data)
                option_num +=1 
            pick = int(input("Masukkan pilihan : "))
            if (pick == 1):
                clear()
                Prodi.sort_prodi_by(attr[1])
            if (pick == 2):
                clear()
                Prodi.sort_prodi_by(attr[0])
            if (pick == 3):
                clear()
                Prodi.sort_prodi_by(attr[3])
            if (pick == 4):
                break
    
    @staticmethod
    def find_prodi(code):
        def confirm(code, sql, val):
            if code != "":
                verify = input("Masukkan kode akses untuk melanjutkan : ")
                if verify == code:
                    cursor.execute(sql, val)
                    print("Kode akses diterima, data diubah")
                else:
                    print("Kode akses salah, data tidak diubah")
            else:
                cursor.execute(sql, val)

        def change_prodi(res, code):
            menu = ['Ubah Nama','Ubah Akreditasi','Ubah Biaya UKT', 'Hapus Data', 'Kembali']
            while True:
                num = 0
                no = 0
                for i in range(len(menu)):
                    print(i+1,". ", menu[i])
                choose = input("Masukkan pilihan anda : ")
                if choose == "1":
                    clear()
                    new_name = input("Masukkan nama prodi baru : ")
                    sql = "UPDATE prodi SET Nama = %s WHERE ID = %s"
                    val = (new_name, res)
                    confirm(code, sql, val)
                    cursor.execute("SELECT * FROM prodi WHERE ID = '{}'".format(res))
                    result = cursor.fetchall()
                    print("-"*99)
                    print(
                        f"| {'No': <4} | {'ID': <15} | {'Nama':<30} | {'Akreditasi': <15} | {'Biaya UKT': <19} |")
                    print("-"*99)
                    for result in result:
                        print(
                            f"| {num+1:<4} | {str(result[0]):<15} | {result[1]:<30} | {result[2]:<15} | Rp. {result[3]: <15} |")
                        num +=1
                    print("-"*99)
                if choose == "2":
                    clear()
                    new_akr = input("Masukkan akreditasi prodi baru : ")
                    sql = "UPDATE prodi SET Akreditasi = %s WHERE ID = %s"
                    val = (new_akr, res)
                    confirm(code, sql, val)
                    cursor.execute("SELECT * FROM prodi WHERE ID = '{}'".format(res))
                    result = cursor.fetchall()
                    print("-"*99)
                    print(
                        f"| {'No': <4} | {'ID': <15} | {'Nama':<30} | {'Akreditasi': <15} | {'Biaya UKT': <19} |")
                    print("-"*99)
                    for result in result:
                        print(
                            f"| {num+1:<4} | {str(result[0]):<15} | {result[1]:<30} | {result[2]:<15} | Rp. {result[3]: <15} |")
                        num +=1
                    print("-"*99)
                if choose == "3":
                    clear()
                    new_akr = int(input("Masukkan biaya UKT prodi baru : "))
                    sql = "UPDATE prodi SET BiayaUKT = %s WHERE ID = %s"
                    val = (new_akr, res)
                    confirm(code, sql, val)
                    cursor.execute("SELECT * FROM prodi WHERE ID = '{}'".format(res))
                    result = cursor.fetchall()
                    print("-"*99)
                    print(
                        f"| {'No': <4} | {'ID': <15} | {'Nama':<30} | {'Akreditasi': <15} | {'Biaya UKT': <19} |")
                    print("-"*99)
                    for result in result:
                        print(
                            f"| {num+1:<4} | {str(result[0]):<15} | {result[1]:<30} | {result[2]:<15} | Rp. {result[3]: <15} |")
                        num +=1
                    print("-"*99)
                if choose == "4":
                    clear()
                    sql = "DELETE FROM prodi WHERE ID = %s"
                    verify = input("Masukkan kode akses untuk melanjutkan : ")
                    if code != "":
                        if verify == code:
                            cursor.execute(sql, (res,))
                            print("Kode akses diterima, data dihapus")
                            input("Tekan enter untuk melanjutkan...")
                        else:
                            print("Kode akses salah, data tidak dihapus")
                    else:
                        cursor.execute(sql, (res,))
                
                if choose == "5":
                    break
                    
        def query_result(result, choose, code):
            num= 0
            if cursor.rowcount != 0:
                print("-"*99)
                print(
                    f"| {'No': <4} | {'ID': <15} | {'Nama':<30} | {'Akreditasi': <15} | {'Biaya UKT': <19} |")
                print("-"*99)
                for result in result:
                    print(
                        f"| {num+1:<4} | {str(result[0]):<15} | {result[1]:<30} | {result[2]:<15} | Rp. {result[3]: <15} |")
                    num +=1
                print("-"*99)
                if choose < 3:
                    change_prodi(result[0], code)
                else:
                    input('Tekan enter untuk kembali...')
            else:
                print('Program studi tidak ditemukan')
                input('Tekan enter untuk kembali...')
        while True:
            clear()
            option = ['ID Program Studi', 'Nama Program Studi', 'Akreditasi Program Studi', 'Kembali']
            attr = ['ID', 'Nama', 'Akreditasi', 'BiayaUKT']
            num = 0
            print('Cari program studi berdasarkan : \n')
            for option in option:
                print(num+1,". ", option)
                num += 1
            choose = int(input('\nMasukkan pilihan anda : '))
            if (choose == 1):
                clear()
                value = input('Masukkan ID program studi yang ingin dicari : ')
                cursor.execute("SELECT * FROM prodi WHERE ID = '{}'".format(value))
                result = cursor.fetchall()
                query_result(result, choose, code)
            if (choose == 2):
                clear()
                value = input('Masukkan nama program studi yang ingin dicari : ')
                cursor.execute("SELECT * FROM prodi WHERE Nama = '{}'".format(value))
                result = cursor.fetchall()
                query_result(result, choose, code)
            if (choose == 3):
                clear()
                value = input('Masukkan akreditasi program studi yang ingin dicari : ')
                cursor.execute("SELECT * FROM prodi WHERE Akreditasi = '{}'".format(value))
                result = cursor.fetchall()
                query_result(result, choose, code)
            if (choose == 4):
                break


clear = lambda: os.system('cls')
code = ""
while True:
    cursor.execute("SELECT * FROM tbapprove")
    approve_code = cursor.fetchone()
    if approve_code != None:
        code = approve_code[0]
    clear()
    user_menu = ['Masuk sebagai Admin', 'Masuk sebagai Mahasiswa', 'Set atau Ganti Kode Akses']
    number = 1
    print("Selamat Datang ! \n")
    for user in user_menu:
        print(number,". ", user)
        number+=1
    user_choose =input("\nMasukkan pilihan : ")
    if (user_choose == '1'):
        while True:
            clear()
            menu = ['Tambah Mahasiswa', 'Tambah Program Studi', 'Tampilkan Mahasiswa', 'Tampilkan Program Studi', 'Cari Mahasiswa', 'Cari Program Studi', 'Keluar']
            count = 1
            print('Selamat Datang!\n')
            for menu in menu:
                print(count,". ", menu)
                count += 1
            choose = int(input("\nMasukkan pilihan : "))
            if choose == 1:
                Mahasiswa.tambah_mhs()
            if choose == 2:
                Prodi.tambah_prodi()
            if choose == 3:
                Mahasiswa.show_mhs()
            if choose == 4:
                Prodi.show_prodi()
            if choose == 5:
                Mahasiswa.find_mhs(code)
            if choose == 6:
                Prodi.find_prodi(code)
            if choose == 7:
                break
    
    if (user_choose == '2'):
        while True:
            clear()
            mhs_menu = ['Tampilkan Mahasiswa', 'Tampilkan Program Studi', 'Keluar']
            count = 1
            print('Selamat Datang!\n')
            for menu in mhs_menu:
                print(count,". ", menu)
                count += 1
            choose = input("\nMasukkan pilihan : ")
            if choose == '1':
                Mahasiswa.show_mhs()
            if choose == '2':
                Prodi.show_prodi()
            if choose == '3':
                break
    
    if (user_choose == '3'):
        clear()
        cursor.execute("SELECT * FROM tbapprove")
        if cursor.rowcount == 0:
            password = input("Set kode akses : ")
            sql = "INSERT INTO tbapprove (Code) VALUES (%s)"
            cursor.execute(sql, (password,))
        else:
            password = input("Masukkan kode akses saat ini : ")
            cursor.execute("SELECT * FROM tbapprove")
            rest = cursor.fetchall()
            if (password,) == rest[0]:
                new_code = input("Masukkan kode akses baru : ")
                sql = "UPDATE tbapprove SET Code = %s"
                cursor.execute(sql, (new_code,))
            else:
                print("Kode salah")
                input("Tekan enter untuk melanjutkan..")
