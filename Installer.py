from pathlib import Path
import requests
import shutil
import os
import sys
import zipfile
import time
import winreg
import ctypes
import argparse


#credit to https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python for the bcolors class!

#----------------My Own Librarys-----------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#-------------------Variables--------------------
standardPathForLuaMacros = 'C:/Program Files (x86)/'

ahkDownloaded = False

programDescription='This is EldosHD´s installer script. You can use it to install his 2nd-Keyboard-Scripts, LuaMacros and Autohotkey. You can customize your installation with -c or --custom. The script will make an entry in your registry so your terminal can display colors. If you dont want the script to edit your registry, use --no-color. If you want to check the code for yourself, or learn more about the script in general, check out my GitHub repo for the script! --> https://github.com/EldosHD/myInstallers.\nThank you for using this installer. Have a good day ;)'
#-------------------Functions--------------------

def downloadFile(url, nameFile):
    r = requests.get(url)

    with open(nameFile , 'wb') as f:                    #öffnet ein neues file namens unzip_test.bat in write bytes (wb) modus im filemanegaer (f)
        f.write(r.content)
    print(bcolors.OKBLUE + '--Finished Download--\n' + bcolors.ENDC)
        
def unZipFiles(fileToUnzip, directoryToUnzipTo):
    print('--Unpacking Zip File--')
    with zipfile.ZipFile(fileToUnzip, 'r') as zipFileToExtract:
        zipFileToExtract.extractall(directoryToUnzipTo)
    print(bcolors.OKBLUE + '--Finished Unpacking--\n' + bcolors.ENDC)  

def getPathAndMove():
    print(bcolors.WARNING + 'Where do you want to install it? (If no path is specefied it will be installed in C:\Program Files (x86))\n' + bcolors.ENDC)
    path = input('NOTE THAT THE PATH HAS TO BE WRITTEN LIKE THIS C:/Folder/Folder/Folder/  <--- Dont forget the last slash\n')
    if path == '':
        path = standardPathForLuaMacros
    elif path.find('/', len(path)-2) == -1: #checks if "/" is in the string (.find() returns -1 if it finds nothing)
        path = path + '/'

    
    if os.path.exists(path):
        print('--Moving luaMacros.zip to ' + path + '--')
        if os.path.exists(path + 'luaMacros.zip'):
            return path
        else:
            shutil.move('luaMacros.zip', path)
    else:
        print(bcolors.FAIL + 'you specified an invalid Path!' + bcolors.ENDC)
        tryAgain = input('Do you want to specify another path? (NOTE if you dont specify a path it will be installed to C:/Program Files (x86)/) (Y/N)')
        if tryAgain.lower() == 'y':
            path = getPathAndMove()
        else:
            path = standardPathForLuaMacros
            shutil.move('luaMacros.zip', path)
    return path

def installAllScripts():
    #cleans up old downloads
    try:        
        paths = ['C:/AHK','C:/master.zip', 'master.zip']
        for path in paths:
            myPath = Path(path)
            if myPath.is_file(): #checks if file exists
                os.remove(myPath)
            elif myPath.is_dir():
                shutil.rmtree(myPath)
    except:
        print(f'{bcolors.FAIL}The cleanup failed!{bcolors.ENDC}')

    print('--Downloading GitHub Repo--')
    try:
        downloadFile('https://github.com/EldosHD/2nd-Keyboard/archive/master.zip', 'master.zip')
    except:
        print(bcolors.FAIL + 'Could not download all scripts. Check your internet connection. Besides, the github Servers could be down too. Check this link: https://github.com/EldosHD/2nd-Keyboard/' + bcolors.ENDC)
        return
    print('--Moving master.zip to C:--')
    
    shutil.move('master.zip', "C:/")
    print(bcolors.OKBLUE + '--Finished Moving--\n'+ bcolors.ENDC)
    unZipFiles('C:/master.zip', 'C:/AHK')
    print('--Installing Scripts--')

    errorCount = 0

    try:
        os.rename('C:/AHK/2nd-Keyboard-master', 'C:/AHK/2nd-keyboard' )
    except:
        print(bcolors.FAIL + 'Failed to rename C:/AHK/2nd-Keyboard-master to C:/AHK/2nd-keyboard' + bcolors.ENDC)
        errorCount += 1
    
    try:
        os.rename('C:/AHK/2nd-keyboard/2nd-Keyboard-Scripts','C:/AHK/2nd-keyboard/LUAMACROS')
    except:
        print(bcolors.FAIL + 'Failed to rename C:/AHK/2nd-keyboard/2nd-Keyboard-Scripts to C:/AHK/2nd-keyboard/LUAMACROS' + bcolors.ENDC)
        errorCount += 1

    try:
        os.remove('C:/AHK/2nd-keyboard/LUAMACROS/.gitattributes')
    except:
        print(bcolors.FAIL + 'Failed to remove: C:/AHK/2nd-keyboard/LUAMACROS/.gitattributes'+ bcolors.ENDC)
        errorCount += 1

    try:
        os.remove('C:/AHK/2nd-keyboard/README.md')
    except:
        print(bcolors.FAIL + 'Failed to remove: C:/AHK/2nd-keyboard/README.md'+ bcolors.ENDC)
        errorCount += 1

    try:
        os.remove('C:/master.zip')
    except:
        print(bcolors.FAIL + 'Failed to remove: C:/master.zip'+ bcolors.ENDC)
        errorCount += 1

    if errorCount == 0:
        print(bcolors.OKBLUE +'--Finished Installing Scripts--\n' + bcolors.ENDC)
        print(bcolors.WARNING + 'NOTE: YOU SHOULD CREATE A SHORTCUT FOR YOUR STARTUP FOLDER!!!\n' + bcolors.ENDC)
    else:
        print(f'There were {bcolors.FAIL + str(errorCount) + bcolors.ENDC} errors!')

def installAHK():
    print('--Downloading Autohotkey--')
    try:
        downloadFile('https://www.autohotkey.com/download/ahk-install.exe', 'AutoHotkeyInstaller.exe')
    except:
        print(bcolors.FAIL + 'Could not download AHK. Check your internet connection. Besides, the Servers could be down too. Check this link: https://www.autohotkey.com/download/' + bcolors.ENDC)
        return False
    print(bcolors.WARNING + 'The AHK installer will run once this application finishes\n' + bcolors.ENDC)
    return True

def installLuaMacros(path):
    print('--Downloading LuaMacros--')

    try:
        downloadFile('http://www.hidmacros.eu/luamacros.zip', 'luaMacros.zip')
    except:
        print(bcolors.FAIL + 'Could not download Lua Macros. Check your internet connection. Besides, the Servers could be down too. Check this link: http://www.hidmacros.eu/luamacros.zip' + bcolors.ENDC)
        return

    print(bcolors.OKBLUE + '--Finished Moving--\n' + bcolors.ENDC)
    unZipFiles(path + 'luaMacros.zip', path + 'luaMacros')
    os.remove(path + 'luaMacros.zip')

def isAdmin():      #credit to: https://raccoon.ninja/en/dev/using-python-to-check-if-the-application-is-running-as-an-administrator/
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

#----------------End of Functions----------------

#----------------Beginn of Program---------------
def main():

    parser = argparse.ArgumentParser(description=programDescription, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c','--custom', default=False, action='store_true', help='asks you which scripts you want to install')
    parser.add_argument('--no-color', default=False, action='store_true', help='removes all color from the output and doesn´t edit your registry')
    parser.add_argument('-p','--path', default=standardPathForLuaMacros, type=str, help='specify the path where you want LuaMacros to be installed')

    args = parser.parse_args()

    #------------------Registry Edit-----------------
    if args.no_color == True:
        bcolors.HEADER = ''
        bcolors.OKBLUE = ''
        bcolors.OKGREEN = ''
        bcolors.WARNING = ''
        bcolors.FAIL = ''
        bcolors.ENDC = ''
        bcolors.BOLD = ''
        bcolors.UNDERLINE = ''
    else:   #changes registry to display colors in cmd
        access_registry = winreg.ConnectRegistry(None,winreg.HKEY_CURRENT_USER)
        access_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Console",0,winreg.KEY_ALL_ACCESS | winreg.KEY_WOW64_64KEY)
        sub_key = r'VirtualTerminalLevel'
        winreg.SetValueEx(access_key, sub_key,0,winreg.REG_DWORD,1041)            

    if args.custom == True:
        print(bcolors.WARNING + 'Note: The following inputs will default to "no" if you enter anything other than "y"!' + bcolors.ENDC)
        print(bcolors.BOLD + 'Welcome to this installer for EldosHD´s scripts. I will guide you through all of this. \n' +bcolors.ENDC)

        allScripts = input('Do you want to install all of EldosHD´s scripts? (Y/N) \n')
        autoHotkey = input('Do you want to install Autohotkey? (Y/N) \n')
        luaMacros = input('Do you want to install LuaMacros? (Y/N) \n')
    else:
        allScripts = 'y'
        autoHotkey = 'y'
        luaMacros = 'y'


#--------------Start of Installing---------------
    if allScripts.lower() == 'y':
        installAllScripts()


    if autoHotkey.lower() == 'y':
        installAHK()


    if luaMacros.lower() == 'y':
        installLuaMacros(args.path)


    print(bcolors.OKGREEN + 'Thank you for using this installer the programm will exit in 3 seconds' + bcolors.ENDC)

#---------------End of Installing----------------
    time.sleep(3)

    if ahkDownloaded:
        try:
            os.system("/AutoHotkeyInstaller.exe")
        except:
            print(bcolors.FAIL + 'Failed to run the AHK installer. Check the folder you are currently in to see if its there. If its not. Download it again and run it.' + bcolors.ENDC)

if __name__ == "__main__":
    if (isAdmin() == False):
        print("The script must run as administrator to work properly.")
        input("Press any key to exit!")
        sys.exit()
    else:
        main()