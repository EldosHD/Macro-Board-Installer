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



#-------------------Variables--------------------
standardPathForLuaMacros = 'C:/Program Files (x86)/'

ahkDownloaded = False

errorCount = 0

programDescription='This is EldosHD´s installer script. You can use it to install his 2nd-Keyboard-Scripts, LuaMacros and Autohotkey. You can customize your installation with -c or --custom. The script will make an entry in your registry so your terminal can display colors. If you dont want the script to edit your registry, use --no-color. If you want to check the code for yourself, or learn more about the script in general, check out my GitHub repo for the script! --> https://github.com/EldosHD/myInstallers.\nThank you for using this installer. Have a good day ;)'

#credit to https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python for the bcolors class!
#----------------My Own Librarys-----------------
class bcolors:
    HEADER = '\033[95m' #unused
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'    #unused
    UNDERLINE = '\033[4m'   #unused
    
    def printFail(self, stringToPrint: str):
        print(bcolors.FAIL + stringToPrint + bcolors.ENDC)
    
    def printWarning(self, stringToPrint: str):
        print(bcolors.WARNING + stringToPrint + bcolors.ENDC)
    
    def printBlue(self, stringToPrint: str):
        print(bcolors.OKBLUE + stringToPrint + bcolors.ENDC)

    def printGreen(self, stringToPrint: str):
        print(bcolors.OKGREEN + stringToPrint + bcolors.ENDC)

#-------------------Functions--------------------

def downloadFile(url, nameFile):
    r = requests.get(url)

    with open(nameFile , 'wb') as f:                    #öffnet ein neues file namens unzip_test.bat in write bytes (wb) modus im filemanegaer (f)
        f.write(r.content)
    bcolors.printBlue('--Finished Download--')
        
def unZipFiles(fileToUnzip, directoryToUnzipTo):
    print('--Unpacking Zip File--')
    with zipfile.ZipFile(fileToUnzip, 'r') as zipFileToExtract:
        zipFileToExtract.extractall(directoryToUnzipTo)
    bcolors.printBlue('--Finished Unpacking--') 

def installAllScripts():
    global errorCount 
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
        bcolors.printFail('The cleanup failed!')
        errorCount += 1

    print('--Downloading GitHub Repo--')
    try:
        downloadFile('https://github.com/EldosHD/2nd-Keyboard/archive/master.zip', 'master.zip')
    except:
        bcolors.printFail('Could not download all scripts. Check your internet connection. Besides, the github Servers could be down too. Check this link: https://github.com/EldosHD/2nd-Keyboard/')
        errorCount += 1
        return
    print('--Moving master.zip to C:--')
    try:
        shutil.move('master.zip', "C:/")
    except:
        bcolors.printFail('Failed to move the code to C:/')
        errorCount += 1
        return
    bcolors.printBlue('--Finished Moving--')
    try:
        unZipFiles('C:/master.zip', 'C:/AHK')
    except:
        bcolors.printFail('Failed to unzip the Source code')
        errorCount += 1
        return
    
    print('--Installing Scripts--')
    try:
        os.rename('C:/AHK/2nd-Keyboard-master', 'C:/AHK/2nd-keyboard' )
    except:
        bcolors.printFail('Failed to rename C:/AHK/2nd-Keyboard-master to C:/AHK/2nd-keyboard')
        errorCount += 1
    
    try:
        os.rename('C:/AHK/2nd-keyboard/2nd-Keyboard-Scripts','C:/AHK/2nd-keyboard/LUAMACROS')
    except:
        bcolors.printFail('Failed to rename C:/AHK/2nd-keyboard/2nd-Keyboard-Scripts to C:/AHK/2nd-keyboard/LUAMACROS')
        errorCount += 1

    try:
        os.remove('C:/AHK/2nd-keyboard/LUAMACROS/.gitattributes')
    except:
        bcolors.printFail('Failed to remove: C:/AHK/2nd-keyboard/LUAMACROS/.gitattributes')
        errorCount += 1

    try:
        os.remove('C:/AHK/2nd-keyboard/README.md')
    except:
        bcolors.printFail('Failed to remove: C:/AHK/2nd-keyboard/README.md')
        errorCount += 1

    try:
        os.remove('C:/master.zip')
    except:
        bcolors.printFail('Failed to remove: C:/master.zip')
        errorCount += 1

    bcolors.printBlue('--Finished Installing Scripts--')
    bcolors.printWarning('NOTE: YOU SHOULD CREATE A SHORTCUT FOR YOUR STARTUP FOLDER!!!')

def installAHK():
    global errorCount
    print('--Downloading Autohotkey--')
    try:
        downloadFile('https://www.autohotkey.com/download/ahk-install.exe', 'AutoHotkeyInstaller.exe')
    except:
        bcolors.printFail('Could not download AHK. Check your internet connection. Besides, the Servers could be down too. Check this link: https://www.autohotkey.com/download/')
        errorCount += 1
        return False
    bcolors.printWarning('The AHK installer will run once this application finishes\n')
    return True

def installLuaMacros(path):
    global errorCount
    print('--Downloading LuaMacros--')

    try:
        downloadFile('http://www.hidmacros.eu/luamacros.zip', 'luaMacros.zip')
    except:
        bcolors.printFail('Could not download Lua Macros. Check your internet connection. Besides, the Servers could be down too. Check this link: http://www.hidmacros.eu/luamacros.zip')
        errorCount += 1
        return
    bcolors.printBlue('--Finished Moving--')

    try:
        unZipFiles(path + 'luaMacros.zip', path + 'luaMacros/')
    except:
        bcolors.printFail('failed to unzip luaMacros.zip')
        errorCount += 1
    try:
        os.remove(path + 'luaMacros.zip')
    except:
        bcolors.printFail('failed to remove luaMacros.zip ')
        errorCount += 1

def isAdmin():      #credit to: https://raccoon.ninja/en/dev/using-python-to-check-if-the-application-is-running-as-an-administrator/
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

#----------------End of Functions----------------

#----------------Beginn of Program---------------
def main():
    global errorCount

    parser = argparse.ArgumentParser(description=programDescription, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('-c','--custom', default=False, action='store_true', help='asks you which scripts you want to install')
    parser.add_argument('--no-color', default=False, action='store_true', help='removes all color from the output and doesn´t edit your registry')
    parser.add_argument('-p','--path', default=standardPathForLuaMacros, type=str, help='specify the path where you want LuaMacros to be installed')

    args = parser.parse_args()

    print(f'PAth: {args.path}')
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
        ahkDownloaded = installAHK()


    if luaMacros.lower() == 'y':
        installLuaMacros(args.path)


#---------------End of Installing----------------
    time.sleep(1)

    if ahkDownloaded:
        try:
            os.system("/AutoHotkeyInstaller.exe")
        except:
            bcolors.printFail('Failed to run the AHK installer. Check the folder you are currently in to see if its there. If its not. Download it again and run it.')
            errorCount += 1
        try:
            os.remove("/AutoHotkeyInstaller.exe")
        except:
            pass

        if errorCount == 0:
            bcolors.printGreen('Installation successfull!')
        else:
            print(f'There were {bcolors.FAIL + str(errorCount) + bcolors.ENDC} errors!')

        
if __name__ == "__main__":
    if (isAdmin() == False):
        print("The script must run as administrator to work properly.")
        input("Press any key to exit!")
        sys.exit()
    else:
        main()