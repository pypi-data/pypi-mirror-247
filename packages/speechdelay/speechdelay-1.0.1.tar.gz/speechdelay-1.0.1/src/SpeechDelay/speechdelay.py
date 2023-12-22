from time import sleep as wait
from colorama import Fore
import os

class funcs():
    def speech(ctx=str(), delay=0.2, wincls=False, clswarning=True, color="WHITE"):
        try:
            if ctx == "":
                print(Fore.YELLOW + "Please enter a string as first arg." + Fore.WHITE)
                return
        except:
            print(Fore.YELLOW + "Please enter a string as first arg." + Fore.WHITE)
            return
        try:
            if delay != float(delay):
                print(Fore.YELLOW + "Please enter a float for second arg." + Fore.WHITE)
                return
        except:
            print(Fore.YELLOW + "Please enter a float for second arg." + Fore.WHITE)
            return
        try:
            if wincls != bool(wincls):
                print(Fore.YELLOW + "please enter a boolean for third arg." + Fore.WHITE)
                return
        except:
            print(Fore.YELLOW + "please enter a boolean for third arg." + Fore.WHITE)
            return
        try:
            if clswarning != bool(clswarning):
                print(Fore.YELLOW + "please enter a boolean for fourth arg." + Fore.WHITE)
                return
        except:
            print(Fore.YELLOW + "please enter a boolean for fourth arg." + Fore.WHITE)
            return
        if wincls:
            if clswarning:
                print(Fore.RED + "WARNING: wincls uses windows terminal commands to clear the terminal and will blink due to the delay of python")
                if input(Fore.WHITE + '\nWould you like to continue? Y/N (will continue if if input is invalid)').lower() == 'n':
                    TypeError("Operation Cancelled")

                else:
                    usrstr = str()
                    for x in list(ctx):
                        os.system("cls")
                        usrstr = usrstr + x
                        if x != " ":
                            try:
                                print(eval("Fore." + color) + usrstr + Fore.WHITE)
                                wait(delay)
                            except:
                                print(Fore.YELLOW + "Please specify a color. For a list of the avaliable colors, please run colors()" + Fore.WHITE)
            
            else:
                usrstr = str()
                for x in list(ctx):
                    os.system("cls")
                    usrstr = usrstr + x
                    if x != " ":
                        try:
                            print(eval("Fore." + color) + usrstr + Fore.WHITE)
                            wait(delay)
                        except:
                            print(Fore.YELLOW + "Please specify a color. For a list of the avaliable colors, please run colors()" + Fore.WHITE)
                    
        else:
            usrstr = str()
            for x in list(ctx):
                usrstr = usrstr + x
                if x != " ":
                    try:
                        print(eval("Fore." + color) + usrstr + Fore.WHITE)
                        wait(delay)
                    except:
                        print(Fore.YELLOW + "Please specify a color. For a list of the avaliable colors, please run colors()" + Fore.WHITE)
        
    def colors(color=None):
        if color == None:
            print(Fore.RED + "\nRED" + Fore.GREEN + "\nGREEN" + Fore.BLUE + "\nBLUE" + Fore.YELLOW + "\nYELLOW" + Fore.MAGENTA + "\nMAGENTA" + Fore.CYAN + "\nCYAN" + Fore.WHITE + "\nWHITE" + Fore.BLACK + "\nBLACK" + Fore.WHITE)
        if color == "RED":
            print(Fore.RED + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)
        if color == "GREEN":
            print(Fore.GREEN + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)
        if color == "BLUE":
            print(Fore.BLUE + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)
        if color == "YELLOW":
            print(Fore.YELLOW + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)
        if color == "MAGENTA":
            print(Fore.MAGENTA + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)
        if color == "CYAN":
            print(Fore.CYAN + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)
        if color == "WHITE":
            print(Fore.WHITE + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)
        if color == "BLACK":
            print(Fore.BLACK + "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!£$%^&*()" + Fore.WHITE)