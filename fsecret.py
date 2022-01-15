from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Random import get_random_bytes as rand
import pathlib
from pwinput import pwinput as getpass
from sys import argv as args
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
	
	try:
		f = open(fn, "rb")
		d = f.read()
		f.close()
	except FileNotFoundError or IsADirectoryError:
		print("Invalid file!")
		return
	
	d_out = b""
	
	if emode:
		if getpass("Please retype the password: ").encode("utf-8") != pwd:
			print("Passwords don't match!")
			return
		d_out = encrypt(key, d)
	else:
		pt = decrypt(key, d)
		if pt == None:
			print("Invalid password!")
			return
		d_out = pt
	f = open(fn, "wb")
	f.write(d_out)
	f.close()
	
	if emode:
		print("The file has been encrypted!")
		return
	
	print("The file has been decrypted!\n You can now use it!")
	
	c = input("Do you want to encrypt it again? Y/n: ")
	
	if not (c == "" or c.lower() == "y" or c.lower() == "yes"):
		return
	
	print("Encrypting...")
	
	f = open(fn, "rb")
	d = f.read()
	f.close()

	d_out = encrypt(key, d)

	f = open(fn, "wb")
	f.write(d_out)
	f.close()

	print("Done.")

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
