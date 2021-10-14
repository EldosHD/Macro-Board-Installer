# Why does this repo exist?
I dont know why you are here. But since you stumbled across my little project you might want to take a look. Here I dump my installer scripts for my other projects.
The only current project is my Makrokeyboard. I created it with the help of Luamacros and I currently use it to trigger and control my scripts for Minecraft 
and as a shortcut for certain folders and apps.
The original code was written by Taran van Hemert. I followed [this](https://www.youtube.com/watch?v=Arn8ExQ2Gjg) Tutorial by Taran and modified his code heavily.
In case you want to check out my code, follow [this](https://github.com/EldosHD/2nd-Keyboard) link.
If you want to try out the program itself, you should watch Tarans Tutorial first, since I wont explain how the program itself functions. 
I will only talk about my Installer for it. You can either install his code manually, or use my installer to download and install Luamacros,
Autohotkey (that´s the language I use to create my makros) and my code.
# What does it do and how do I use it?
The program is written in Python. You should use the .exe file since you probably have to install the Python librarys otherwise. 
It uses the command line, because I think thats cooler than using a GUI (And its less work). I will explain what the code does and how you
can customize your installation. Since Autohotkey sadly only works on windows, this Installer is Windows only too. But you can try it on Linux and send me the results LOL ;)
## Step 1
Start a cmd or powershell as administrator. The program will install stuff in your C: drive and therefore needs admin privileges.
## Step 2 
Go to the location of the installer script.
## Step 3
You can type SCRIPTNAME for a full installation and skip the other steps. Or you can type SCRIPTNAME -c or --custom for a quick custom installation. **BUT** the installer will
change your registry. I wanted to use colored text and the simplest solution was using a [class](https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-python?page=1&tab=votes#tab-top) created by Joeld on stack overflow.
To use this color codes I had to make a small tweak to the registry.
I added to HKEY_CURRENT_USER/Console/VirtualTerminalLevel the value 1041. (Idk why, but this makes the colors function) If you don´t want to change the registry, use option --no-color. If you want to know more type SCRIPTNAME --help.
## Step 4 (Only for custom installation)
At first the program will ask you if you want to install my scripts. Thats the reason why this script exists, so you should type y or Y. If you type anything else it will consider it as no.
The program will ask if you want to install Autohotkey. If you type y the script will download the installer and launch it after it is done. 
Last but not least you will be asked if you want to install Luamacros. Type y if it isn´t installed already, since it and Autohotkey are both required for my script to function.
If you only typed y for my scripts the installer will install them in C:/AHK and exit. **NOTE:** You should create a shortcut for my scripts and lua macros in your startup folder since the installer (currently) doesn´t handle that for you.
## Step 5 (only if you typed y for luamacros)
The script will ask you where to install it. If you leave it blank, it will install it to C:\Program Files (x86).
**NOTE**: The path has to be written linke this: C:/Folder/Folder/Folder/  <--- Dont forget the last slash
# Done
Now you have my scripts. You will most likely have to modify my code for your needs.
I used these librarys:
- argparse
- ctypes
- os
- Path from pathlib
- requests
- shutil
- sys
- time
- winreg
- zipfile
