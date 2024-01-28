#Author - Sagnik Chandra
# """
# PassSwift: A Python script for streamlined password management tasks.
#
# This script provides several functionalities for password management:
# - Password generation: Generate strong passwords with customizable criteria.
# - Password strength checker: Evaluate the strength of passwords based on various criteria.
# - Password wordlist check: Check if a password is present in a common wordlist.
# - Secure password storage: Encrypt and store passwords with website and username in a file.
# - Password file reading: Read and decrypt passwords stored in the password file.
# - Hash method identification: Identify the hash method (algorithm) of a given hash value.
#
# Author: Sagnik Chandra.
# GitHub: https://github.com/MIISTERC
# Instagram: https://www.instagram.com/sc17_kali/
#
# Usage:
# - Run the script and follow the interactive menu prompts to perform password management tasks.
# - Ensure that you have the required dependencies installed. See requirements.txt for details.
#
#
import os
import time 
import string
import random
from colorama import Fore,Style
import sys
import secrets
from cryptography.fernet import Fernet
import re
def pasgen():
    print(Fore.YELLOW + Style.BRIGHT + "<==[INFO!] Generate a strong password of your choice !! and leave inputs field blank for using default values.==>")
    c1 = input("[*] Add letters : [y/n] : ") or "y"
    c2 = input("[*] Add numbers : [y/n] : ") or "y"
    c3 = input("[*] Add special characters : [y/n] : ") or "y"
    chars = ""
    if c1.lower() == "y":
        chars += string.ascii_letters
    if c2.lower() == "y":
        chars += string.digits
    if c3.lower() == "y":
        chars += string.punctuation
    try:
       length = int(input("[*] Enter length of the password [Reccommended 15] : "))
    except ValueError:
       print("[*] Proper length not given, using default value '15'. ")
       length = 15
    try:
       ask = int(input("[*] How many passwords do you want ? : "))
    except ValueError:
       print("[*] Using default value '1'.")
       ask = 1
    for i in range(ask):
       password = ""
       password = ''.join([secrets.choice(chars) for _ in range(length)])
       print(f"[*] Password generated : {password}")
    print("[*] Press Enter to go back to Menu.")
    ask = input(">>") or "99"
    if ask == 99:
       print_banner()
    else:
       print_banner()
           

def pastren():
    print(Fore.GREEN + Style.BRIGHT + "<==[Note!] Blank spaces are not Accepted in this password strength checker..==>")
    password = input("Enter password : ")
    pt = 0
    res = ""
    if len(password) >= 12:
        pt+=1
    if any(char.isdigit() for char in password):
        pt+=1
    if any(char.isupper() for char in password):
        pt+=1
    if any(char.islower() for char in password):
        pt+=1
    if any(char in "!@#$%^&*()_+-=[]{}|;:,./<>?'" for char in password):
        pt+=1
    if pt<=2:
        res = "Password strength : Very Weak."
    elif pt==3:
        res = "Password strength : Weak."
    elif pt==4:
        res = "Password strength : Strong."
    else:
        res = "password strength : Uncrackable."
    if not password:
        res = "No password provided."
    print("[*] " + res)
    print("[*] Press Enter to go back to Menu.")
    ask = input(">>") or "99"
    if ask == 99:
        print_banner()
    else:
        print_banner()
def chpas(): 
    print(Fore.RED + Style.BRIGHT + "<==[!INFO] This functions checks whether your password is present in commonly used password list.==>")
    password = input("[*] Enter password : ")
    path = input("[*] /path/to/the/wordlist? : [leave blank for default] : ") or "wordlist.txt"
    
    try:
        with open(path,"r",encoding="ISO-8859-1") as passf:
           print("[*] Scanning The Wordlist..")
           pas = passf.read().splitlines()
           print("[*] Searching in the wordlist. Be patience..")
           time.sleep(3)
           if password in pas:
              print("[*] Password Found in the wordlist, Change the password immediately.")
           else:
              print("[*] Password Not found in wordlist.")
           
    except FileNotFoundError:
       print("[*] Cant open wordlist..")
    print("[*] Press Enter to go back to Menu.")
    ask = input(">>") or "99"
    if ask == 99:
        print_banner()
    else:
        print_banner()

def gkey():
    return Fernet.generate_key()
def lkey():
    key_path = ".Key.key"
    if os.path.exists(key_path):
        return open(key_path,'rb').read()
    else:
        key = gkey()
        with open(key_path,'wb') as kf:
            kf.write(key)
        return key
def epassweb(usr,web,passw,key):
    cs = Fernet(key)
    eweb = cs.encrypt(web.encode())
    epass = cs.encrypt(passw.encode())
    eusr = cs.encrypt(usr.encode())
    return eusr,eweb,epass
def dpassweb(eusr,eweb,epass,key):
    cs = Fernet(key)
    dweb = cs.decrypt(eweb).decode()
    dpass = cs.decrypt(epass).decode()
    dusr = cs.decrypt(eusr).decode()
    return dusr,dweb,dpass
def spassweb(usr,web,passw):
    key = lkey()
    eusr,eweb,epass = epassweb(usr,web,passw,key)
    with open("password.txt",'ab') as file:
        file.write(eusr + b'\n' + eweb + b'\n' + epass + b'\n')
def rpas():
    key = lkey()
    password = []
    if os.path.exists("password.txt"):
        with open("password.txt",'rb') as rfile:
            enc_pass = rfile.read().split(b'\n')
            for i in range(0,len(enc_pass) -1,3):
               eusr = enc_pass[i]
               eweb = enc_pass[i + 1]
               epass = enc_pass[i + 2]
               dusr,dweb,dpass = dpassweb(eusr,eweb,epass,key)
               password.append((dusr,dweb,dpass))
        return password
def checkhash():
    print(Fore.LIGHTRED_EX + Style.BRIGHT + "<==[!INFO] This Function Identify The method(Algorithm) of a hash given as Input by the User...==> ")
    hash_value = input("Enter the hash : ")
    md5 = re.compile(r'^[a-fA-F0-9]{32}$')
    sha1 = re.compile(r'^[a-fA-F0-9]{40}$')
    sha256 = re.compile(r'^[a-fA-F0-9]{64}$')
    method = ""
    if md5.match(hash_value):
        method = "MD5"
    elif sha1.match(hash_value):
        method = "SHA1"
    elif sha256.match(hash_value):
        method = "SHA256"
    else:
        method = "unkown method"
    print(f"The Method Of the Hash : {method}")
    print("[*] Press Enter to go back to Menu.")
    ask = input(">>") or "99"
    if ask == 99:
        print_banner()
    else:
        print_banner()

def print_banner():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
    banner = r'''
__________                        _________       .__  _____  __   
\______   \_____    ______ ______/   _____/_  _  _|__|/ ____\/  |_ 
 |     ___/\__  \  /  ___//  ___/\_____  \\ \/ \/ /  \   __\\   __\
 |    |     / __ \_\___ \ \___ \ /        \\     /|  ||  |   |  | 
 |____|    (____  /____  >____  >_______  / \/\_/ |__||__|   |__|  
                \/     \/     \/        \/                         
'''
    print(Fore.BLUE + Style.BRIGHT + banner)

# Call the function to print the banner in red
    print(Fore.MAGENTA + Style.BRIGHT + "Version 1.0")
    print("Author - MIISTERC")
    print("Github - https://github.com/MIISTERC")
    print("Press Ctrl + C to exit.")
    print(Fore.BLUE + "="*70)
    print(Fore.WHITE + Style.BRIGHT + "Menu :-")
    print("1.Password Generator.")
    print("2.Password Strength Checker.")
    print("3.Check Password in a Wordlist.")  
    print("4.Save Password in Password File.")
    print("5.Read The Password File.")
    print("6.Identify Hash Method. ")
    print(Fore.BLUE + "="*70)
    print(Fore.GREEN + Style.BRIGHT + "[*] (1/2/3/4/5/6)?..")
    try:
        choice = input(Fore.WHITE + "PassSwift~# ")
    except KeyboardInterrupt:
        print("\n[*] Ctrl + C detected , Exiting now.")
        sys.exit(1)
    if(choice == "1"):
        pasgen()
    elif(choice == "2"):
        pastren()
    elif(choice == "3"):
        chpas()
    elif(choice == "4"):
        print(Fore.MAGENTA + Style.BRIGHT + "<==[!INFO] Save and encrypt yor password and website in the password.txt file.==>")
        web = input("[*] Enter website name for which the password you are saving (e.g google.com) :  ")
        usr = input("[*] Enter Username : ")
        pas = input("[*] Enter the password for That Website and Username you are Storing : ")
        spassweb(usr,web,pas)
        print('[*] Saved Successfully.')
        print("[*] Press Enter to go back to Menu.")
        ask = input(">>") or "99"
        if ask == 99:
            print_banner()
        else:
            print_banner()
    elif(choice == "5"):
        saved_passwords = rpas()
        if saved_passwords:
            print("[*] Saved Passwords : ")
            for i,(username,website,password) in enumerate(saved_passwords,1):
                print(f"{i}. Username : {username} ,Website : {website} ,Password : {password}")
        else:
            print("No passwords in the Passwords file.")
        print("[*] Press Enter to go back to Menu.")
        ask = input(">>") or "99"
        if ask == 99:
            print_banner()
        else:
            print_banner()

        
    elif(choice == "6"):
        checkhash()
    else:
        print_banner()

print_banner()



       
    


    




