# PunchOut-RL
This is a class project aimed to train an Reinforcement Learning Agent to beat the Classic NES Mike Tyson's Punch-Out!! game. This is a class project aimed to learn the applications of reinforcement learning

## Prerequisites

Before setting up the project, ensure you have the following:

- **Operating System**: Linux-based environment (e.g., Ubuntu 22.04, WSL2 on Windows)
- **Python Version**: Python 3.10 
- **Package Manager**: `pip` (ensure it's up-to-date with `pip install --upgrade pip`)

### Install Linux-based environment on Windows (preferably Ubuntu 22.04 distro)
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/28Ei63qtquQ/0.jpg)](https://www.youtube.com/watch?v=28Ei63qtquQ)

## Getting Started

### 1. Install Stable-Retro
- Open **Terminal** in your Linux environment
- Update packages
```bash
sudo apt-get update
```

- Install Pip
```bash
sudo apt-get install python3-pip
```

- Verify that you have the correct version of Python installed, run:

```bash
python3 --version
```

- Setup editor with Linux-Based Environemnt <br>
[Visual Studio Code](https://code.visualstudio.com/docs/remote/wsl) <br>
[PyCharm](https://www.jetbrains.com/help/pycharm/using-wsl-as-a-remote-interpreter.html)

### Clone the git repo and open the project folder while connected to the WSL server in your editor

### Open a terminal in your python editor and run this command in that terminal (Not linux bash!)

- Upgrade pip, setuptools, and wheel:
```bash
pip install --upgrade pip setuptools wheel
```

- Create a Virtual Environment: <br>
- Navigate to your project directory and create a virtual environment:
```bash
python3 -m venv venv
```
and activate the venv
```bash
source venv/bin/activate
```

- Install Stable-retro and the required libraries
```bash
pip install -r requirements.txt
```

### 2. Set Up the ROM File
- Copy the rom (.nes) file 
```bash
cp PunchOut.nes venv/lib/python3.10/site-packages/retro/data/stable/PunchOut-Nes/
cd venv/lib/python3.10/site-packages/retro/data/stable/PunchOut-Nes/
mv PunchOut.nes rom.nes
cd ~/PunchOut-RL
```

### 3. Download necessary visual files
- Run these commands in linux bash for your wsl distro
```bash
sudo apt-get install libglu1-mesa libgl1-mesa-glx
sudo apt-get install libgl1-mesa-dev libglu1-mesa-dev
sudo apt-get install python3-opengl
```
