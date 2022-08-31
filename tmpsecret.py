from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Random import get_random_bytes as rand
import pathlib
from pwinput import pwinput as getpass
from sys import argv as args
from tempfile import NamedTemporaryFile
import subprocess
import argparse

def main():
    parser = argparse.ArgumentParser(description="Encrypt files with AES-GCM.")
    parser.add_argument("file", type=pathlib.Path)
    parser.add_argument("-e", "--encrypt", dest="encrypt", action="store_true", help="Encrypt the file instead of decrypting it.")
    
    args = vars(parser.parse_args())
    fn = args.get("file").absolute()
    emode = args.get("encrypt")
    
    pwd = getpass().encode("utf-8")
    key = SHA3_256.new(pwd).digest()
    
    f = open(fn, "rb")
    d = f.read()
    f.close()
    
    if emode and fn.exists() and fn.is_file():
        if getpass("Please retype the password: ").encode("utf-8") != pwd:
            print("Passwords don't match!")
            return
        d_out = encrypt(key, d)
        f = open(fn, "wb")
        f.write(d_out)
        f.close()
        print("File encrypted.")
        return
    elif emode:
        print("Not a file!")
        return
    
    pt = decrypt(key, d)
    if pt == None:
        print("Invalid password!")
        return
    
    with NamedTemporaryFile() as tmp:
        tmp.write(pt)
        tmp.flush()
        subprocess.run(["vim", tmp.name])
        tmp.seek(0)
        td = tmp.read()
        d_out = encrypt(key, td)
        f = open(fn, "wb")
        f.write(d_out)
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
