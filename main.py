from tkinter import *
from cryptography.fernet import Fernet

BG = 'gray60'

root = Tk()
root.geometry('400x205')
root.title('Secure Independent Storage')
root.resizable(False, False)
root['bg'] = BG
root.eval('tk::PlaceWindow . center')

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
    text = text.encode()

    cipher_key = make_key()
    try:  cipher = Fernet(cipher_key)
    except:
        insert('Insert Key')
        return

    encrypted_text = cipher.encrypt(text)

    return encrypted_text.decode('utf-8')

def decrypt_data():
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
    encrypted = encrypt_data()
    if encrypted:
        insert(encrypted)

def decrypt():
    decrypted = decrypt_data()
    if decrypted:
        insert(decrypted)

def encrypt_and_write(): # SOON
    encrypted = encrypt_data()
    if encrypted:
        insert(encrypted)
    

data_var = StringVar(root)
key_var = StringVar(root)

Label(root, text='Data:', bg=BG, font='Arial 12').place(x=5, y=10)
Label(root, text='Key:', bg=BG, font='Arial 12').place(x=5, y=40)

Entry(root, width=50, textvariable=data_var, bg='gray70', border=0).place(x=50, y=14)
Entry(root, width=50, textvariable=key_var, bg='gray70', border=0).place(x=50, y=44)

Button(root, text='Encrypt', command=encrypt, bg=BG, activebackground='gray70').place(x=10, y=70)
Button(root, text='Decrypt', command=decrypt, bg=BG, activebackground='gray70').place(x=70, y=70)

text = Text(width=48, height=6, bg='gray')
text.configure(state='disabled')
text.place(x=5, y=100)

root.mainloop()