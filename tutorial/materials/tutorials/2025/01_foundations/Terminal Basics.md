## Learning Objectives 
By the end of this Terminal Introduction, you should be able to:
- Explain key terminology (directory, root, console, terminal, shell) and understand how they relate 
- Recognize the motivation for using the terminal instead of only a graphical interface (efficiency, automation, remote access)
- Set up Bash on your system 
- Distinguish between absolute and relative paths and understand when to use each for navigation 
- Navigate the file system by interpreting path structures and directory hierarchy
### Important Terminology 
- Directory:
	- a way of organizing and storing files on your computer 
	- contains files and/or other directories (subdirectories)
	- helps keep related files together so you don't have everything in one place
	- you can move, rename, or delete directories just like files
> **In Plain English**:
> - a "folder" on your computer where files and other folders live 

- Root:
	- top-level directory in a file system 
	- every other directory and file stems from this point, like branches from a tree
	- you cannot go "higher" than root - it's the starting point of the file structure
> **In Plain English**:
> - the "home base" or very top folder from which all other folders and files branch out

- Console:
	- the physical device that allows you to interact with the computer 
>**In Plain English**: 
>- it's your computer screen, keyboard, and mouse 
>- you - the user - interact with your computer *through* your console 

- Terminal:
	- a text input and output environment 
	- program that allows us to enter commands that the computer processes 
	- since it is a program, you can install it and uninstall it as you please 
	- you can also have many terminals installed in your computer and run whichever you want whenever you want 
>**In Plain English:**
>- the "window" in which you enter the actual commands your computer will process 

- Shell:
	- program that acts as command-line interpreter 
	- processes commands and outputs the results 
	- interprets and processes the commands entered by the user 
	- a program that can be installed and uninstalled by the user 
		- different shells -> different syntax and characteristics 
	- Linux and Mac use the default shell Bash while on Windows it's normally Powershell 
		- to use the Linux Bash shell on your computer that uses Windows type `wsl`
	- Shells work as programming languages, in the sense that with them we can build scripts to make our computer execute a certain tasks 
> **In Plain English:**
> - the shell is the program your computer uses to "understand" and execute your commands, and that you can also use it to program tasks 

**Important Note - Terminal vs. Shell:**
 - the terminal is the program in which the shell will run but both programs are independent
 - I can have any shell run on any terminal

### Motivation
- On most computers you have a graphical user interface (GUI) meaning that you can see things on the screen and click around to do whatever we want
- So, why bother learning this complicated terminal-shell thing?
- Advantages of the terminal:
	1. It's more efficient 
		- Some tasks would require many clicks around different windows while these tasks can be executed with a single command 
		- Being comfortable with the command line will help you save time and be able to execute your tasks quicker 
	2. Tasks can easily be automated 
		- We can build scripts with the shell and later on execute those scripts whenever we want 
		- Useful when dealing with repetitive tasks that we don't want to do over and over again
	3. Sometimes it's the only way in which you will be able to interact with a computer 
		- You can easily connect to platforms like GitHub to connect your computer with a remote repository 

### Installation Guide for everyone not using Linux or Mac 
- We will be using Bash in the tutorial so if you are on Windows, the easiest way to get it is by installing WSL (Windows Subsystem for Linux)
- Step by Step: 
	1. Check your Windows Version
		- WSL works best on Windows 10 (updated) or Windows 11
		- Press `Windows Key + R` and type `winver` and press `Enter`
			- If your Windows 10 version is older than 1903, you may need to update before WSL works 
	2. Open PowerShell as Administrator 
		- After checking your Windows version press `Windows Key`, type *PowerShell*, right click it and choose *Run as Administrator*
	3. Install WSL
		- Run the following command: `wsl --install`
			- This will enable the Windows Subsystem for Linux
			- Download Ubuntu 
			- Install Git (needed later - see Tutorial on Git / GitHub)
	4. Restart your computer when prompted 
	5. Finish Ubuntu Setup
		- When your computer restarts, an Ubuntu terminal will open
			- Pick a username (lowercase is easiest)
			- Choose a password 
	6. Test your Bash 
		- Open Ubuntu from the Start menu
		- Type: `echo "Hello from Bash!"` -> if you see the message , you're ready to go

>**Excursus - Ubuntu:** 
>-  An operating system - a layer of software on a computer that acts as a foundation for computer programs (MacOS and Windows are the most common operating systems)
>- Linux is an alternative operating system that is open source
>	- open source means the disclosure of source code so that every interested user/developer is able to modify and further develop and use the source code provided 
>	- As a result, the source code is available for free for everyone
>- Ubuntu is a distribution of Linux
>	- it is a commercial project based on the Linux kernel
>	- the mission is to provide a software platform that is free for users and developers 
>	- you can just install Ubuntu on a computer for free 

❗️**Important Note**:
- Last year some students had a few issues 
- WSL might not work for you especially if you have an older Windows 10 version because the command `wsl --install` downloads the latest WSL version, but some older Windows 10 laptops can't run it 
- If it is not working for you don't stress, the purpose of WSL is that it lets you type the **exact** same commands as in the tutorial and it installs Git automatically 
- So if you don't have WSL you can just do the following: 
	1. You can just look up the Windows equivalent of some Linux commands 
	2. Install Git manually (see Git/GitHub Introduction Tutorial)
	
- also: **please contact us** if you have problems with setting up WSL 

### Opening the terminal 
**Windows**:
- `right click` the windows logo in your taskbar 
- Select `Terminal`or `Terminal (Admin)`
- Type `bash` and hit enter to open the Linux subsystem

**Linux**:
- `press`the super key on your keyboard (on most keyboards this is the key with the windows logo on it)
- Type `terminal`into the search field and press `enter`

**MacOS**:
- `click`the launchpad icon in your dock
- Type `terminal` into the search field and press `enter`

Of course, there are a few other ways of opening the terminal on your respective machine. Some require less input from your side but you might have to first perform a small setup. Here are some sources documenting different approaches for each major OS: [Windows](https://www.howtogeek.com/662611/9-ways-to-open-powershell-in-windows-10/#create-a-powershell-shortcut-on-the-desktop), [Linux](https://www.redhat.com/sysadmin/linux-terminal-window), [MacOS](https://support.apple.com/guide/terminal/open-or-quit-terminal-apd5265185d-f365-44cb-8b09-71a064a42125/mac)

## Some First Steps in the Terminal 

>❗️Keep in mind❗️
> - the following commands are all based on Bash 
> - but most commands should apply to most configurations anyway
> - furthermore: if you decide to use a different Shell you can google the equivalent commands 

- after opening the terminal you should be confronted with a new window looking somewhat like this (*Please note: this a Mac Example, the terminal might look different on your machine*)
- ![Terminal_Example](Terminal-Example.png)
### Navigating the File System Using the Terminal

- Everything in front or - when using a Mac - behind the `:` symbol tells you where the location or source directory you are currently at is
- there are two ways of defining a location:
	1. Absolute path 
	2. Relative path

> **Take an initial guess**:
> Look at the two following paths. Which of them is relative and which is absolute?: 
> 1. `~/Users/Fake/documents/icss<3/session101/command_line.ipynb`
> 2. `icss<3/session101/command_line.ipynb`

- Absolute path: full path from the root directory to the file or directory (Nr.1)
- Relative path: Directions from current location (Nr.2)
- Using the relative path is often the preferred way
	- Saves a lot of typing and reduces room for errors 
	- But in order to do so you need a correct starting location 

> **Visualization**:
> Imagine you want to go from Constance to Berlin. There is no direct trip for that itinerary - you must transfer (e.g., in Baden-Baden). The ticket can either show the entire journey (Constance -> Baden-Baden -> Berlin) or just simply Constance -> Baden-Baden or Baden-Baden -> Berlin)
> - Absolute Path: the absolute path is like the full travel itinerary
> 	- it is like a train ticket that lists the entire journey: Constance -> Baden-Baden -> Berlin
> 	- no matter where your ticket is checked, it is always valid because it covers the complete route 
> 	- in the terminal, it's the exact path from root to destination
> - Relative Path: the relative path is like a partial travel ticket
> 	- ticket covers only part of the journey 
> 	- e.g. you only have a ticket from Baden-Baden -> Berlin 
> 		- you would face a problem if your ticket was checked on the way from Constance to Baden-Baden
> 		- if it were checked on the way from Baden-Baden to Berlin, though, everything would be fine 
> 	- in terminals, it works only relative to your current directory 

- transferring this visualization now to the terminal for navigating your file system using the terminal 
- for the following part we will assume that the correct file path to your target file `command_line.ipynb` is `~/Users/Fake/documents/icss<3/session101/command_line.ipynb`

***Absolute Path***:
- documents each single step from the very start of your journey to the very end of it
- for our example:
```
~/Users/Fake/documents/icss<3/session101/command_line.ipynb
```
- `~`: home directory / parent directory of all other directories 
-> afterwards we just follow the directories (folders) until we reach the directory that contains the file: go to `Users` than go to `Fake` then `documents` then `icss<3` then `session101`. We then can select the file `command_line.ipynb` from the `session101` directory
=> no matter where along the way you might be you will always have a 'valid ticket' since each location aka directory and your target file is listed on your ticket

***Relative Path****:
- documents only a part of your journey from a certain point until the end 
- for example we are already at `~/Users/Fake` 
- then we only have to go to `icss<3` and then `session101` and then we can select the file `command_line.ipynb` from the `session101` directory