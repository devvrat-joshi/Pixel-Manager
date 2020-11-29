# **Pixel Manager**
---
Welcome to the **Pixel Manager**, a lightweight console based file manager for **Linux systems!** This has been developed as a part of the CS 301 Operating Systems Course, IIT Gandhinagar by [Arpita Kabra](https://github.com/arpitakabra), [Devvrat Joshi](https://github.com/devvrat-joshi), [Viraj Shah](https://github.com/viraj-shah18) and [Vrutik Shah](https://github.com/VrutikShah).


## Table of contents
1. [Installation](#install)
2. [Features](#features)
    1. [File Management System](#fms)
    2. [Terminal](#terminal)
    3. [Editor](#editor)
    4. [File Search](#seach)
3. [All Commands](#cmds)
4. [Statistics and Comparision](#stats)


The main features of the Pixel Manager are:


* **File System Management**
* **Built-In Terminal**
* **Built-In File Editor**
* **Quick File Search**


---
## **Installing Pixel Manager**<a name="install"></a>
1. Clone this repository
```
git clone https://github.com/devvrat-joshi/Pixel-Manager.git
```

2. Navigate to the folder
```
cd Pixel-Manager
```

3. Run `make` This will automatically install dependencies as well as run the pixel manager. In case make does not work. Try running
```
python3 main.py
```

4. If it runs into any error, try running `Ctrl + c` to restore into normal state. Run it again to exit from the File Manager!



---
## **Main Features Explained** <a name="features"></a>

### File Management System <a name="fms"></a>
The main window of the File Manager provides an easy way to navigate through any files and directories on the system. The **left panel** shows the contents of the current directory, and highlights the selected content with green color. The **center panel** is for search window and shows the contents of the selected directory (if not a file). The right panel shows stats of the selected file/directory along with CPU and RAM usage. Here is the preview of the main window:
<div><center>File Manager Main window</center></div>

![](https://i.imgur.com/8Lg3hDT.png)


<!-- ![](https://i.imgur.com/DWGzr99.png) -->


Navigate using the arrow keys!
Right key opens to the selected directory and left key moves back to the previous directory.
<div><center>Scrolling through current directory</center></div>

![](https://i.imgur.com/cVEDObI.png)

The bottom row bar displays all the possible commands to **copy, move, delete and create new** files and folders, **search** through directories, and start the **Terminal!**


---
### Terminal <a name="terminal"></a>
The built-in terminal can be toggled by pressing `Shift+TAB`
It can run all Linux commands and system calls. It can also execute user defined programs. However, it does not support interactive programs yet. 

Here's a preview of how it looks:
<div><center>Terminal Preview</center></div>

![](https://i.imgur.com/ZyAFvJ3.jpg)

<!-- ![](https://i.imgur.com/uEXrgoD.png) -->

The input can be given at the bottom most line and the output will be presented in the **Terminal Output** panel. The terminal panel becomes *orange* if your program is still executing. The terminal also supports scrolling if the output is more than the screen size.

---
### Editor <a name="editor"></a>
To edit files on the go, navigate to the file and pressing ```e``` would open the file in the built-in editor. The editor is line-by-line scrollable and we have made sure to handle several corner cases that may arise. 

The current editor is customized for python files, highlighting keywords, adding indentation spaces and auto-completing brackets and strings.
<div><center>Editor Preview</center></div>

![Editor Screenshot](https://i.imgur.com/Xk9uae3.png)

The editor currently also supports cut/copy/paste and find-replace utilities. Following are the screenshots for the same.
<div><center>Selecting Lines</center></div>

![Selecting Files](https://i.imgur.com/K8Y5SRk.png)

<div><center>Highlighting the found words</center></div>

![Highlighting the found words](https://i.imgur.com/anyautJ.png)


---
### Quick Search <a name="search"></a>

To enable the search bar, enter `ctrl + a`. It initiates a trie creation from the current folder in a different process. As soon as the trie is created, it is returned to the main process (the File Manager) to initiate the search. Larger the folder size, larger the size of the trie and more RAM used for storing. However, once created, the trie is stored for further use in **Pickle File** format which uses very less space and saves trie creation time!
Here is a preview of search!
<div><center>Search Preview</center></div>

![](https://i.imgur.com/IpmRXbI.png)

The top bar shows the trie creation process!

Here is how searching looks:
<div><center>Searching through files/folders</center></div>

![](https://i.imgur.com/cX3IztT.png)

It can search for thousands of files giving results instantly. Scroll and navigate through the found items. 

---
## **List of All Commands** <a name="cmds"></a>

### In the Manager


| Command                           | Action                                    |
| --------------------------------- | ----------------------------------------- |
| ```Arrows Keys```                 | Navigate through the files                |
| `e`      (when on a file)         | Open the file editor                      |
| `g`                               | Create a new folder                       |
| `c`                               | Copy the current file or folder           |
| `k`                               | Create a new file                         |
| `m`                               | Move the current file or folder           |
| `v`                               | Paste the cut/copied item                 |
| `d+r` (will ask for confirmation) | Delete the current File or Folder         |
| `Shift + TAB`                     | Open the terminal                         |
| `Ctrl + a`                        | Start a search within the selected folder |
| `END` key                         | Close the Pixel Manager                   |



### In the Terminal
| Command  | Action |
| -------- | -------- |
|`Shift+Tab`   |   Start Terminal   |   
|  `Shift+Tab`|        Close Terminal           |
|`Enter` |To execute the command|
|`Up Down Arrow Keys`|To scroll through the output of terminal|
|`Esc`|To return control to terminal after viewing output in terminal window|




### In the Editor

**Normal Mode**
| Command  | Action       |
| -------- | ------------ |
| `e`      | Start editor |
| `Ctrl+F` | Find         |
| `Ctrl+R` | Replace Text |
| `Escape` | Enter Command Mode|

**Command Mode**
| Command | Action                                 |
| ------- | -------------------------------------- |
| `s`     | Enter Visual Mode (for cut/copy/paste) |
| `i`     | Enter normal Mode                      |
| `q`     | Quit Editor (option to save and discard changes)|

**Visual Mode**
| Command  | Action                   |
| -------- | ------------------------ |
| `c`      | Copy Text                |
| `x`      | Cut Text                 |
| `v`      | Paste Text               |
| `Escape` | To return to normal mode |


### During Search
| Command              | Action                           |
| -------------------- | -------------------------------- |
| `Ctrl+a`             | To begin search                  |
| `Ctrl+a`             | To return from search            |
| `Up Down Arrow Keys` | To scroll through search results |
| `Enter`              | To navigate to any search result |

---
## **Some Statistics** <a name="stats"></a>

![](https://i.imgur.com/QwRTwxc.png)
.

     

![](https://i.imgur.com/9mACGxs.png)

---
### <div><center>[Link to the Presentation](https://drive.google.com/file/d/1FU9KvMKyhQhalqbKgY0ikj8BSvyUCex4/view?usp=sharing) </div></center>
---
