## Learning Objectives: 
By the end of the session, you will be able to:
- Understand what Git is and why version control is important
- Explain the difference between local and remote repositories
- Set up Git and configure it correctly (including SSH keys)
- Clone a repository from GitHub to your local machine 
- Track changes using Git commands (`status`,`add`,`commit`)
- Push and Pull updates between your local and remote repositories 
- Handle basic collaboration workflows using GitHub
- Create a GitHub repository and connect it to your local Git repository 
## Introduction

### What is Git?
- Git is a software for version control
- version control helps you manage changes to files over time - especially code, text, or projects with multiple collaborators 
	- it tracks changes 
	- saves snapshots; so you can go back to previous versions 
	- prevents mistakes by letting you experiment in branches without breaking the main project
	- shows who changed what, when, and why
	- helps teams collaborate safely and efficiently 
### What is GitHub?
 **Platform for Collaboration**
- platform to share and collaborate on code and to collaboratively work on code with project partners/colleagues
 **Remote Storage**
- remote platform (comparable to a "cloud") to back up your code, ensuring that your work is safe and accessible from anywhere 

> **Excursus - Local vs. Remote:** 
> *Local Machine*: 
> - fancy way of saying your own computer, as opposed to a server or computer somewhere else (like in the cloud or on the internet)
> *Remote Machine*:
> - another computer you connect to (e.g., a server, GitHub, a cloud machine)

## Basic Concepts 
### Working Directory
- a folder on your laptop (local machine) in the file system where you make changes to your project files 
- represents a snapshot of your repository at a specific point in time 
- this is where you make changes to your files before sending it to the remote machine 
### Repository 
- a repository is a database that stores all the information about the changes made to your project over time -> it includes the entire history of changes you made 
- there we also distinguish between the **local** and the **remote** repository 
	**Local Repository:**
		- a hidden **`.git`** folder within your working directory that saves snapshots of your project 
		- it contains all projects files and commit history
	**Remote Repository:** 
		- copy of the local repository hosted on a service like GitHub
		- these allow you to collaborate with others, share your code, and back up your work
### How GitHub works with Repositories
- GitHub hosts remote repositories where you can "upload" (push) your "local changes" (commits) to a remote repository and "get" (pull) changes (updates) from it to keep your local machine up to date

> **Visualization:**
>  Think of GitHub as a central library where you can store your books (repositories). You can check out books (pull changes) to read and make notes (commit changes), and then return them to the library (push changes) for others to access.

- in this class GitHub will be primarily used to exchange files 
	- **Submissions Repository**: You will push your assignments to a **`submissions-YourName`** repository and pull updates (Feedback to your assignments) as needed.
	- **Materials Repository**: You will pull course materials from a designated repository but won't push changes to it.
## Why Data Scientist should use Version Control
- since it helps to maintain a history of changes and tracks changes to source code using Version Control enables you to look at old snapshots of a project 
	- this way you can check why certain changes were made and if you then connect it with a collaborative website and work on projects together with others, it is nice to have in order to see what other people have changed 
	- you can also see why certain modifications were made, who made them, and when -> this is useful for understanding the evolution of a project and for debugging 

> **Visualization:**
> Version control is like a time machine for your project. You can travel back to any previous snapshot to see the state of your project at that time, understand the changes made, and even revert to an earlier version if needed.

- Why Git? -> Git is the most widely used version control system globally, with a market share of around 70% 

## Installing and Setting Up Git / Github
### Git Installation
- we have to install [git](https://git-scm.com/downloads) in order to use **`git-commands`** via the terminal
- on Linux and Mac git is usually pre-installed and Windows users should have gotten it by installing WSL
- you can check if git is installed and which version of git is installed with the following command in your terminal -> **`git --version`**
	- To Do - only if git is NOT installed 
		**Windows**
		- visit the [git homepage](https://git-scm.com/downloads)
		- download the installer and execute it 
		- you don't need  **`custom installation`** !!
		**MacOS**
		- install [homebrew](https://brew.sh/)
		- restart your terminal after installing homebrew
		- after installing homebrew just follow the instructions on the git installation page
		- enter **`brew install git`** into your terminal

❗️**Important for Windows Users**
- there will come a point where git asks you whether it should use the default Windows terminal application for its execution 
- make sure to enable the option **`Use Windows' default console window`**

### SSH Key 
**Basic Explanations**
- SSH is a protocol used to securely connect to remote serves over the internet 
	- it provides a secure channel over an unsecured network by using cryptographic techniques
- an SSH key can be understood as your id-card to identify yourself
	- it is a pair of cryptographic keys used for authentication
- there is a **private** and a **public** key
	❗️DO NOT SHARE YOUR PRIVATE KEY❗️
- in order to identify yourself you will give GitHub your public key while your local machine keeps the private one 
- this is your way of authentication so that you can "upload" (push) and "download" (pull) stuff from your laptop to the repositories of your GitHub account and vice versa 
	- when you want to access a remote repository, your local machine uses the private key to authenticate with the remote server
	- the remote server verifies the private key against the public key it has on record, granting access if they match 

>**Visualization**
> GitHub is like a club who has your name on the guest list for an amazing party (public key). When you want to enter a party you show your id with name & photo, to prove that you are the person listed on the guest list (private key).

### Set Up SSH Connection to GitHub - Step by Step
**Overview of all the Steps we need to do:**
1. Create a [Github Account](https://github.com/join) 
2. Create an [SSH key pair](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)  (if you haven't already)
3. Add your public [SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
4. [Check connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)

**Step 1 - Create a Github Account:**
- pretty self-explanatory
- only necessary if you don't have one already 
-  if you are registering for the first time, it would be best to use your university email address, but this is not a requirement

**Step 2 - Create an SSH Key pair:**
- check if you already have an SSH key pair
	- enter the command **`ls -al ~/.ssh`** in the terminal
	- if you already have an SSH key pair you will get a list with the contents of your `.ssh` directory
		- look for files like:
			- `id_rsa` and `id_rsa.pub` (RSA key pair)
		    - `id_ed25519` and `id_ed25519.pub` (modern key pair)
		    - `id_dsa`, `id_ecdsa`, etc.
		- files ending in `.pub` are the **public keys**
		- the ones without the extension are the **private keys** (keep them secret!)
- if you already have an SSH key you can now go to Step 3
- now for those of you that don't have an SSH key pair
	1. Open your terminal
	2. Enter `ssh-keygen -t ed25519 -C "your_email@example.com"`
		❗️Don't forget to input your own email - especially the one you used to create your GitHub account with 
	- you will be prompted to enter a name and a password for your key
		❗️You don't have to do that, just press `enter` without inputting anything
		- if you decide to change the name of your key files or add a password be aware that you will have to input the whole file path and just the name because otherwise there won't be saved in the default `.ssh` directory but in the working directory of your terminal (this might cause issues down the line
>**Note:**
>Windows and Mac file explorer often hide the `.ssh` folder, so you have to change the explorers setting to also show so-called `hidden files`
> *Windows* : in the explorer, select `View` - `Show` - `Hidden Items`
> *Mac*: in the respective folder, where you want to show the subfolders press `Command` + `Shift` + `.`

**Step 3 - Add your public SSH key to your Github Account**
1. Navigate to the location of your SSH key pair
	- you should be able to see the file path documented in the terminal output of the above command
	- or restart your terminal and enter the following command: **`ls -al ~/.ssh`** 
2. Get the content of the public SSH key 
	- if you have RSA key pair (`id_rsa.pub`)
		- enter the command **`cat ~/.ssh/id_rsa.pub`** in the terminal 
	- otherwise, if you have a modern key pair (`id_ed25519.pub`)
		- enter the command **`cat ~/.ssh/id_ed25519.pub`**
	- copy the entire output you get of your **public** SSH Key
3. Copy the content of your public SSH key to your GitHub account
	- Log in on [GitHub](https://www.github.com)
	- Click on your profile in the top right
	- Navigate to 'Settings'
	- Navigate to 'SSH and GPG Keys'
	- Select 'New SSH Key'
		- *Title*: Give the Key a name 
		- *Key type*: just leave it as 'Authentication Key'
		- *Key*: Paste the content of your **public** (the output you got in Step 2) SSH key here 
	- Select 'Add SSH key'

**Step 4 - Check Connection**
1. Open your terminal 
2. Type `ssh - T git@github.com` into your terminal
- if you have never connected to GitHub via SSH you will get a message along the lines "`authenticity of host 'gihub.com...' can't be established`"
	- just type `yes` into your terminal and hit `enter`
- if everything works as it should you will see a message like: 
	`Hi! You've successfully authenticated...`

>**Note**
> The setup of Git, GitHub and the SSH connection is **essential**.
> So, if something doesn't work, you have any problems or open questions just ask!

## Working with Git and GitHub - The most important steps 

### Cloning to your local machine
- after building a connection between your local machine and GitHub you can now use the tool of cloning a repository in order to create a local copy of the remote repository on your machine 
- this allows you to work on the project locally 
- furthermore, this way you can "download" (pull) all the material quite easily and "upload" (push) your assignments to your submission repository 

*Step by Step - Clone a Repository:* 
1. **Copy Repository URL:**
	- Navigate to the repository on GitHub
	- Click on the "Code" button, choose SSH and copy the repository URL
2. **Open Terminal:** 
	- open your terminal or command prompt
	- navigate to the directory you want to save your file in 
3. **Clone Repository:** 
	- Run the following command where you replace **`<repository-url>`**  with the URL you copied
		```
		git clone <repository-url>
		```
### Pulling Updates
- when talking about download there was always this word **pull** in brackets 
- we are now introducing this expression; one of the most important expressions while using Git and GitHub
- Pulling updates ensures that your local repository is synchronized with the latest changes from the remote repository 
- it is like downloading something from a platform

*Step by Step - Pull Updates:*
1. **Open Terminal:**
	- Navigate to your local repository directory in the terminal
2. **Pull Updates:**
	- run the following command
		```
		Kopieren 
		git pull origin main
		```
3. **Resolve Conflicts:**
	- if there are conflicts, Git will notify you
	- conflicts and conflict resolutions are a bit tricky with Git and GitHub; we will talk about it later when we handle advanced topics in Git and GitHub
	- so for now: contact us if you get a conflict message 
### Committing and Pushing Changes 
- now we will talk about the upload - the right term in the context of Git and GitHub to **push**
- this allows you to save your work locally and save it or share it with others in the remote repository 

*Step by Step - Push Updates:*
1. **Stage Changes**:
	- use `git status` to check the status of your working directory 
		❗️**IMPORTANT**❗️
		- if there are things in the remote repository that have not been pulled to the local repository yet pull those first !!
		- this is super important because otherwise conflicts will arise
		- we will always push a feedback file for your assignments so you will need to pull that first before uploading the new assignment
	- Stage all changes you want to commit: 
		```
		Kopieren 
		git add .
		```
	- (you can also only stage the changes you want to commit with the following command: `git add <file>`, but for now always staging all changes is the best to do)

>**Excursus - Staging Area**:
>- this is often confusing for beginners
>- it's where you prepare the changes you want to include in your next snapshot (commit)
>- Git will see any file you change, but only the staged changes (changes that you add with the command `git add`) will be committed 
>- it is like a waiting room for changes
>- that means until you run `git add`, Git is just watching - not saving

2. **Commit Changes:**
	- commit the staged changes with a descriptive message (e.g. `submission-a01`)
		```
		Kopieren 
		git commit -m "Descriptive commit message"
		```
3. **Push Changes:**
	- push the committed changes to the remote repository: 
		```
		Kopieren 
		git push origin main
		```

> **Excursus - Ignoring Files with `.gitignore`**
> - Sometimes you have files you don't want to include in your commits.
> - Create a file named `.gitignore` in your repository and in there you write down everything you want to ignore when committing.
> - Git will then ignore anything matching these patterns. 
### Creating a Git Repository from Scratch
- another way to start a brand new project is to initialize a local repository as a Git repository 
- so now, we are not cloning from GitHub but setting everything up on our local machine
- with `git init` we can turn any local folder into a Git repository

**Steps to create a Git repository**
1. Optional: Create a new directory 
2. Navigate to your new directory or an already existing one in your terminal
3. Run the following command: `git init`

- this creates a hidden `.git` folder that tracks all changes 
	- so when you run `ls` in the directory you won't see the hidden `.git` file but you can see it when you run `ls -a` since it shows all the hidden files 
	- with `ls .git` you can look what is stored in that hidden file
- you can now add files, commit them, and even connect this repo to GitHub later with: `git remote add origin...`
### Creating a GitHub Repository
- you don't need to create your own repository for this course 
- this is just for you, as you will reach a point later in your data science career where you will need to create your own repository

**Steps to create a repository**
1. Log in to GitHub: 
	- go to [**GitHub**](https://github.com/) and log in with your account
2. Create a new repository:
	- click on the "+" icon in the top-right corner and select "New repository"
	- provide a repository name, description, and choose whether it should be public or private
	- initialize the repository with a README file if desired
 
 >**Excursus - README file**:
 >A README file is a plain text or Markdown (md) placed in the root of your project folder. It explains what the project is, how to use it, how to install and run it and any other important details. 
 
3. Repository settings:
	- (optionally), you can add a **`.gitignore`** file and choose a license for your project 
4. Create Repository 

>**Best Practice**:
>Use descriptive names for your repositories to make it clear what the project is about.
>For your later work life: 
>	- Always include a README file that provides an overview of the project, setup instructions, and how to contribute (❗️you do not need to do this for the repositories in our ICSS course)
>	- choose an appropriate license to specify how others can use your code 

## Overview of the courses repositories 
### Submission Repository 
- this one can simply be cloned by you 
- everyone has an own repository 
- you pull to receive the feedback 
- you push to upload your code solutions 

### Materials Repository 
- here, you only have the right to pull content, because we all share it and we do not want you to overwrite our materials 
- but since we want you to solve hands-on tasks in the tutorial notebooks, you need to fork that repository 
- for you it is enough to know that forking means making a copy of the repository, which belongs to someone else 
	- this way you get a repository with the same name, but now, it belongs to your account
		- this one, you can now clone
		- you sync the fork, to get updates from the original repo
		- this allows you to make changes to the repository without affecting the original project 
- if you created a fork, you can just simply pull each week, solve the hands-on tasks without getting any conflicts 

*Step by Step - Create a fork of materials*:
1. **Fork a Repository:**
	- navigate to the repository you want to fork on GitHub 
	- Click the "Fork" button in the top-right corner 
2. **Clone the Forked Repository:**
	- clone the forked repository to your local machine
        ```
        Kopieren
        git clone <your-forked-repository-url>
        ```
❗️Before you can pull content from the forked repository you always have to update it

## Exercises
After setting up Git and your GitHub: here are some exercises you can try yourself — because **"practice makes perfect"**:
1. Create a GitHub repository
	- On GitHub, create a new repository called `git-practice` 
	- Clone it to your local machine using SSH
2. Work in the cloned folder
	- Open your terminal and navigate into the cloned folder
	- Inside, create a new text file called 'HelloGitHub.txt' and add some content (e.g., "Hello from Git!")
	- Stage and Commit this file 
		- Try to choose a commit message that makes sense
	- Push the change to GitHub
**BONUS TASK**
After completing these basic steps, it’s time to get an impression of how collaboration workflows can look on GitHub.  
In the following tasks, you’ll work with a classmate to simulate how developers collaborate in real life.
3. Pair up and take first steps
	- Pair up with a classmate and decide who will be Person A.
	- Person A: 
		- Creates a new public GitHub repository called `collab-practice` 
		- Adds a simple text file (e.g. called `greetings.txt`) with a message like "Hello from *insert your name*!"
		- Commits and pushes it to GitHub
4. Fork the repository 
	- Person B: 
		- Goes to Person A's repository on GitHub
		- Clicks Fork to create a personal copy under their own GitHub account
5. Clone the Fork
	- B clones their own fork of A's repo to their local machine
	- Open `greetings.txt.` and verify it contains A's message.
6. Make a change 
	- Person B:
		- Creates a new file called `reply.txt` with a message like: "Hi ..., nice repo!"  
		- Stages, commits (with a meaningful commit message), and pushes the file to their own fork.
7.  Pull the change
	- Now it’s Person A’s turn to pull in the change.
	- Person B shares the **GitHub URL** of their fork with Person A.
	- Person A adds B’s fork as a remote and fetches it:
	```
	git remote add b *Insert GitHub Url*
	git fetch b
	```
	- Person A pulls the changes from B’s fork into a new local branch:
	```
	git checkout -b b-changes b/main
	```
	- Person A can now review the changes and merge them into their own project if desired.
