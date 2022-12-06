# Initiation Connection

# User Authentication NIP & Password
    # Jika hasil true
        # notif masukan data sigakerja
    # Jika hasil false
        # return notif login false
    # End

# [nip, password, tanggal, jam_mulai, jam_akhir, urtug, keterangan]

# user : /start
# What you gonna do
# user : /login nip pass
# Input the date start 
# user : 20-12-2022
# Input the date end
# user : 20-12-2022
# Input Jam Mulai
# user : 08:00
# Input Jam Selesai
# user : 10:00
# get urtug
# Masukan nomor urtug
# user : nomor
# Masukan keterangan
# user : keterangan
# data sudah dimasukan.

import requests
import json
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.filters import Filters
from getpass import getpass
from datetime import date

payload = {}
  
updater = Updater("5650387427:AAGJ8ezUudJLIUuXWRZwZhEF9fyfNab1FGA", use_context=True)

# start function
def start(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Untuk mengisi sigakerja kamu bisa mengirim /tglmulai tanggal-bulan-tahun, contohnya /tglmulai 01-12-2022")

def login(update: Update, context: CallbackContext):

    user = context.args[0]
    password = context.args[1]

    payload = {'nip': user, 'password': password}

    r = requests.post("http://sikerja.kemendagri.go.id/auth/login", data=payload, timeout=60, verify=False)
    cookie = r.headers["Set-Cookie"]
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://sikerja.kemendagri.go.id',
                'Referer': 'http://sikerja.kemendagri.go.id/transaksi/home2/add',
                'Cookie': cookie}
    respons = json.loads(r.text)
    status = respons["status"]

    if status:
        update.message.reply_text( "Sudah berhasil login")
        update.message.reply_text( "Silahkan kirim tanggal dengan format /tglmulai tanggal-bulan-tahun")
    else:
        update.message.reply_text( "Oops, check kembali NIP dan Password anda.")

    # print(respons["status"] == 1)


def unknown(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Sorry Boss '%s' gak ada didalam perintah gw." % update.message.text)
  
  
def unknown_text(update: Update, context: CallbackContext):
    update.message.reply_text(
        "Ehhh siapa lu gw gak kenal , apaan tuh '%s'" % update.message.text)

def tglmulai(update: Update, context: CallbackContext):
    if not context.args : update.message.reply_text("Anda belum masukan tanggal mulai!!!")
    else:
        payload['data_sender[tgl_mulai_raw]'] = context.args[0]
        update.message.reply_text("Tanggal mulai, udah gw simpan.")
        update.message.reply_text("Lalu kirim tanggal selesai, dengan format /tglselesai tanggal-bulan-tahun")

def tglselesai(update: Update, context: CallbackContext):
    if not context.args : update.message.reply_text("Anda belum masukan tanggal selesai!!!")
    else:
        payload['data_sender[tgl_selesai_raw]'] = context.args[0]
        update.message.reply_text("Tanggal selesai, udah gw simpan")
        update.message.reply_text("Sekarang masukan jam mulai, dengan format /jammulai 08:00")

def jam_mulai(update: Update, context: CallbackContext):
    if not context.args : update.message.reply_text("Anda belum masukan jam mulai!!!")
    else:
        payload['data_sender[jam_mulai]'] = context.args[0]
        update.message.reply_text("Jam mulai, udah gw simpan.")
        update.message.reply_text("Sekarang masukan jam selesai, dengan format /jamselesai 16:00")

def jam_selesai(update: Update, context: CallbackContext):
    if not context.args : update.message.reply_text("Anda belum masukan jam selesai!!!")
    else:
        payload['data_sender[jam_selesai]'] = context.args[0]
        update.message.reply_text("Jam selesai, udah gw simpan.")
        update.message.reply_text("Sekarang masukan keterangan pekerjaan, dengan format /keterangan keterangan kerjaan. Sebentar, gw kirim contoh formatnya...")
        update.message.reply_text("/keterangan Melakukan koordinasi yang penting")

def urtug(update: Update, context: CallbackContext):
    if not context.args : update.message.reply_text("Anda belum masukan nomor uraian tugas!!!")
    else:
        payload['data_sender[urtug]'] = context.args[0]
        update.message.reply_text("Nomor uraian tugas, udah gw simpan.")
        update.message.reply_text("Untuk melihat datanya kamu dapat melihat dengan kirim /lihatdata")

def keterangan(update: Update, context: CallbackContext):
    if not context.args : update.message.reply_text("Anda belum masukan keterangan!!!")
    else:
        payload['data_sender[ket_pekerjaan]'] = ' '.join(context.args[0:])
        update.message.reply_text("Keterangan, udah gw simpan.")
        update.message.reply_text("Sekarang masukan nomor uraian tugas. Untuk melihat bisa dengan /listurtug. Untuk default bisa gunakan /urtug 356281 (Melaksanakan tugas yang diberikan atasan, baik secara lisan maupun tulisan)")

def lihatData(update: Update, context: CallbackContext):
    try:
        data = {
            "Nomor uraian tugas" : payload['data_sender[urtug]'],
            "Tanggal mulai" : payload['data_sender[tgl_mulai_raw]'],
            "Tanggal selesai" : payload['data_sender[tgl_selesai_raw]'],
            "Jam mulai" : payload['data_sender[jam_mulai]'],
            "Jam selesai"  : payload['data_sender[jam_selesai]'],
            "Keterangan kerjaan" : payload['data_sender[ket_pekerjaan]']
        }
        update.message.reply_text(data)
        update.message.reply_text("Untuk simpan data, silahkan balas dengan format /simpan NIP password. Sebentar, gw kirim contoh formatnya...")
        update.message.reply_text("/simpan 199212212020112013 inipassword")
        update.message.reply_text("Kalau mau hapus, silahkan kirim /hapus")
    except KeyError as ke:
        update.message.reply_text("Isi data dulu sampai akhir Boss!!")


def simpanData(update: Update, context: CallbackContext):
    user = context.args[0]
    password = context.args[1]

    global payload

    auth = {'nip': user, 'password': password}

    r = requests.post("http://sikerja.kemendagri.go.id/auth/login", data=auth, timeout=60, verify=False)
    cookie = r.headers["Set-Cookie"]
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'http://sikerja.kemendagri.go.id',
                'Referer': 'http://sikerja.kemendagri.go.id/transaksi/home2/add',
                'Cookie': cookie}

    payload['data_sender[flag_urtug]'] = ''
    payload['data_sender[kuantitas]']  = '0'
    payload['data_sender[file_pendukung]'] = ''

    r = requests.post("http://sikerja.kemendagri.go.id/transaksi/add_pekerjaan_without_file/", data=payload, headers=header, timeout=60, verify=False)

    respons = json.loads(r.text)
    status = respons["status"]

    if status:
        update.message.reply_text( "Sudah berhasil login")
    else:
       update.message.reply_text( "Oops, check kembali NIP dan Password anda.")
       return

    if respons["status"] == 1 : 
        update.message.reply_text("Sudah selesai Boss, udah gw masukin ke sigakerja!! Kalau gak percaya cek aja.")
        update.message.reply_text("Mau isi lagi ?? klik /start")
        payload = {}
        return
    else:
        update.message.reply_text("Sepertinya ada yang salah deh. Coba ulangi lagi mulai dari /start.")
        payload = {}
        return

def hapusData(update: Update, context: CallbackContext):
    payload = {}
    update.message.reply_text("Data telah dihapus, silahkan coba ulangi pengisian data di /start.")

def cekdong(update: Update, context: CallbackContext):
    header = {
        'User-Agent': 'Dalvik/2.1.0(Linux;U;Android 9; Mi A2 Lite Build/PKQ1.180917.001)',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'Origin': 'http://sikerja.kemendagri.go.id',
        'Host': 'ropeg.setjen.kemendagri.go.id',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip',
        'Content-Length': '109'
    }

    # url = 'https://ropeg.setjen.kemendagri.go.id/restsimpeg/api/bni_history_absen'
    url = 'https://ropeg.setjen.kemendagri.go.id/restsimpeg/index.php/ssoview/cek_fp/' + context.args[0] + '/' + context.args[1]

    r = requests.post(url)
    print(r.text)

# Calling command
# Start
updater.dispatcher.add_handler(CommandHandler('start', start))

# Login
updater.dispatcher.add_handler(CommandHandler('login', login))

# Insert tanggal
updater.dispatcher.add_handler(CommandHandler('tglmulai', tglmulai))
updater.dispatcher.add_handler(CommandHandler('tglselesai', tglselesai))

# Insert Jam
updater.dispatcher.add_handler(CommandHandler('jammulai', jam_mulai))
updater.dispatcher.add_handler(CommandHandler('jamselesai', jam_selesai))

# Insert Keterangan
updater.dispatcher.add_handler(CommandHandler('keterangan', keterangan))

# Input Urtug
updater.dispatcher.add_handler(CommandHandler('urtug', urtug))

# Lihat Data
updater.dispatcher.add_handler(CommandHandler('lihatdata', lihatData))

# Simpan Data
updater.dispatcher.add_handler(CommandHandler('simpan', simpanData))

# Hapus Data
updater.dispatcher.add_handler(CommandHandler('hapus', hapusData))

# Check Data Absen
updater.dispatcher.add_handler(CommandHandler('cekdong', cekdong))


updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown))
updater.dispatcher.add_handler(MessageHandler(
    Filters.command, unknown))  # Filters out unknown commands
  
# Filters out unknown messages.
updater.dispatcher.add_handler(MessageHandler(Filters.text, unknown_text))

updater.start_polling()
