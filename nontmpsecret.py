from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Random import get_random_bytes as rand
import pathlib
from pwinput import pwinput as getpass
from sys import argv as args
from tempfile import NamedTemporaryFile
import subprocess

def main():
    print("WARNING: The file is shortly visible in plain text while editing!!\nIf possible, use tmpsecret instead!")
    if len(args) < 2:
        print("Please enter a file name!")
        return
    
    fn = pathlib.Path(args[1])
    pwd = getpass().encode("utf-8")
    key = SHA3_256.new(pwd).digest()
    
    if not (fn.exists() and fn.is_file()):
        if getpass("Please retype the password: ").encode("utf-8") != pwd:
            print("Passwords don't match!")
            return
        d_out = encrypt(key, "Have fun with your new file!".encode("utf8"))
        f = open(fn, "wb")
        f.write(d_out)
        f.close()
        print("New file created.")
        return
    
    f = open(fn, "rb")
    d = f.read()
    f.close()
    
    pt = decrypt(key, d)
    if pt == None:
        print("Invalid password!")
        return
    
    f = open(fn, "wb")
    f.write(pt)
    f.close()
    
    subprocess.run(["vim", fn])

    f = open(fn, "rb")
    pt = f.read()
    f.close()
    
    f = open(fn, "wb")
    f.write(encrypt(key, pt))
    f.close()
    
    print("Encrypted.")

def encrypt(key, d):
    d_out = b""
    nonce = rand(12)
    
    d_out += nonce
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    ct, tag = cipher.encrypt_and_digest(d)
    
    d_out += tag
    d_out += ct
    return d_out

def decrypt(key, d):
    nonce = d[:12]
    tag = d[12:28]
    ct = d[28:]
    
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        pt = cipher.decrypt_and_verify(ct, tag)
    except ValueError:
        return None
    
    return pt

if __name__ == "__main__":
    main()
