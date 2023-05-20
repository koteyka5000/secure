from tkinter import *
from tkinter import messagebox as mb
from cryptography.fernet import Fernet
import json
"""
Варианты использования:


Сообщение в Data и ключ в Key:
    Нажать Encrypt - Зашифровать сообщение Data используя ключ Key и вывести зашифрованное сообщение в поле вывода

    Нажать Decrypt - Расшифровать сообщение Data используя ключ Key и вывести расшифрованное сообщение в поле вывода

    
Сообщение в Data, ключ в Key и имя в Name:
    Нажать Encrypt - Зашифровать сообщение Data используя ключ Key, вывести зашифрованное сообщение в поле вывода, а также записать
                     его в файл data.json с именем Name (чтобы потом получить по имени)

    Нажать Decrypt - |Поле Data игнорируется| Получить зашифрованное сообщение из файла data.json под именем Name, после чего расшифровать
                      используя ключ Key и вывести расшифрованное сообщение в поле вывода

Ключ в Key и имя в Name:
    Нажать Decrypt - Получить зашифрованное сообщение из файла data.json под именем Name, после чего расшифровать
                     используя ключ Key и вывести расшифрованное сообщение в поле вывода
"""
BG = 'gray60'

# Проверка файла ==
try:
    open('data.json', 'r')
except:
    if mb.askyesno('Нет файла', f"В текущей директори нету файла data.json, создать его? Основная директория файла:\n{__file__[:-7]}\n?"):
        with open('data.json', 'x') as f:
            json.dump({}, f)
        mb.showinfo('File Fixed', "Cоздан файл data.json")
    else:
        exit()


# =================

root = Tk()
root.geometry('400x205')
root.title('Secure Independent Storage')
root.resizable(False, False)
root['bg'] = BG
root.eval('tk::PlaceWindow . center')


def fix_file():
    with open('data.json', 'w') as f:
        json.dump({}, f)

def read_from_file():
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except:
        if mb.askyesno('Error in the File', 'Невозможно прочитать файл с данными, отформатировать его? \nЭто удалит все данные!'):
            fix_file()
        insert('File Fixed')
        return {}
    return data


def write_to_file():
    name = name_var.get()
    try:
        with open('data.json', 'r') as f:
            data = json.load(f)
    except:
        if mb.askyesno('Error in the File', 'Невозможно прочитать файл с данными, отформатировать его? \nЭто удалит все данные!'):
            fix_file()
            data = {}
        else:
            return   

    if name in data:
        insert('Name already exists')
        return
    
    enc_data = encrypt_data()
    
    data[name] = enc_data
    
    with open('data.json', 'w') as f:
        json.dump(data, f)

def insert(s):
    text.configure(state='normal')
    text.delete(1.0, END)
    text.insert(INSERT, s)
    text.configure(state='disabled')

def make_key():
    key = key_var.get()
    key = (key * 44)[:43] + '='
    return key

def encrypt_data():
    text = data_var.get()
    if text.replace(' ', '') == '':
        insert('Insert Data')
        return
    
    text = text.encode()
    

    cipher_key = make_key()
    try:  cipher = Fernet(cipher_key)
    except:
        insert('Insert Key')
        return

    encrypted_text = cipher.encrypt(text)

    return encrypted_text.decode('utf-8')

def decrypt_data(_text=None):
    if _text:
        text = _text
    else:
        text = data_var.get()

    cipher_key = make_key()

    try:  cipher = Fernet(cipher_key)
    except:
        insert('Insert Key')
        return
        
    
    try:  decrypted_text = cipher.decrypt(text).decode('utf-8')
    except:
        insert('Fail')
        return
    
    return decrypted_text

def encrypt():
    name = name_var.get()

    encrypted = encrypt_data()

    
    if encrypted:
        insert(encrypted)

        if name:
            write_to_file()

def decrypt():
    name = name_var.get()
    if name:
        data_from_file = read_from_file()
        try:
            decrypted = decrypt_data(data_from_file[name])
        except KeyError:
            insert(f'Name "{name}" not found')
            return
    else:
        decrypted = decrypt_data()
    if decrypted:
        insert(decrypted)
    

data_var = StringVar(root)
key_var = StringVar(root)
name_var = StringVar(root)

Label(root, text='Data:', bg=BG, font='Arial 12').place(x=5, y=10)
Label(root, text='Key:',  bg=BG, font='Arial 12').place(x=5, y=40)
Label(root, text='Name:', bg=BG, font='Arial 12').place(x=210, y=40)

Entry(root, width=50, textvariable=data_var, bg='gray70', border=0).place(x=50, y=14)
Entry(root, width=25, textvariable=key_var,  bg='gray70', border=0).place(x=50, y=44)
Entry(root, width=14, textvariable=name_var, bg='gray70', border=0).place(x=265, y=44)

Button(root, text='Encrypt', command=encrypt, bg=BG, activebackground='gray70').place(x=10, y=70)
Button(root, text='Decrypt', command=decrypt, bg=BG, activebackground='gray70').place(x=70, y=70)

text = Text(width=48, height=6, bg='gray')
text.configure(state='disabled')
text.place(x=5, y=100)

root.mainloop()