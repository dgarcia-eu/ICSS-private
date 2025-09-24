### **Step - by - Step - Pushing the Assignments**
1. Navigate to your submission directory 
2. Make sure you pulled everything: `git status`
	- if not: pull all changes before pushing your assignment: `git pull` 
3. Add your new content to Git: `git add .`
4. Commit your changes: `git commit -m 'submission a0x'`
5. Push your assignment to GitHub: `git push` 
### **Fast Help**
-> **`git help`** : opens general Git help
-> **`git help <command>`**: gets detailed help on a specific Git command
### **Initializing and Cloning Repositories**
-> **`git init`**: initialize a new Git repository in the current directory
-> **`git clone <repositroy-url>`**: clone a remote repository to your local machine
### **Checking Status and Staging Changes**
-> **`git status`**: shows the status of your working directory and staging area
-> **`git add <file>`**: stages specific changes
->**`git add .`**: stages all changes in the current directory
### **Committing Changes**
-> **`git commit -m "message"`**: commits staged changes with a message 
> **Best Practice**: write clear, descriptive commit messages
### **Pushing and Pulling Changes**
-> **`git push`** pushes local commits to the remote branch
-> **`git pull`**: fetch and merge changes from the remote repository 
### **Fetching Without Merging** 
-> **`git fetch`**: downloads remote changes without merging 
### **Branch Management**
-> **`git branch`**: lists all local branches 
-> **`git branch <name>`**: create a new branch
-> **`git checkout <branch>`**: switches to another branch
-> **`git checkout -b <name>`**: creates and switches to a new branch
### **Inspecting History & Differences**
-> **`git log`**: shows commit history 
-> **`git log --all --graph --decorate`**: visualizes commit history 
-> **`git diff`**: shows file changes (unstaged vs staged vs last commit)
### **Merging & Resetting**
-> **`git merge <branch>`**: merge the given branch into the current one 
-> **`git reset`**: unstages files but keep changes 
-> **`git reset --hard`**: discards all changes and resets to last commit (❗️be careful)
### **Ignoring Files**
-> **`.gitignore`**: defines ignores files (e.g., logs, secrets, build folders)
>**Best Practice**: ignore sensitive files (e.g. `.env`, API keys) and keep repositories clean of generated or unnecessary content 
