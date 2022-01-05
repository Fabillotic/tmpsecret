# tmpsecret
Create secret files with a password and open them as a temp file in vim

## Installation
Install the ```pycryptodome``` and ```pwinput``` packages with pip.
```python -m pip install pycryptodome pwinput```

### Making an executable
If you want to create a executable you also need to install ```pyinstaller```.
```python -m pip install pyinstaller```

Now run pyinstaller. Note: the module name ```PyInstaller``` is case-sensitive!
```python -m PyInstaller -F tmpsecret.py```

You'll now find your executable in the ```dist/``` folder.
Add it to PATH and you're done!

## Use
If you have made an executable and added it to PATH you can use ```tmpsecret [some file]``` to access a secret file.
Otherwise invoke ```python``` with ```tmpsecret.py``` ```python tmpsecret.py [some file]```.
If the specified file does not exist, the program will make a new file.
Otherwise it will attempt to decrypt the file with the given password.

If the file already exists, once you enter the command and enter your password, ```vim``` will open and saving+exiting will bring you back to the program which will reencrypt your file.
If you are making a new file, then you will see ```New file created.``` and you can retype the command to access this new file.
