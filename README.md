# PunchOut-RL
This is a class project aimed to train an Reinforcement Learning Agent to beat the Classic NES Mike Tyson's Punch-Out!! game. This is a class project aimed to learn the applications of reinforcement learning

## Prerequisites

Before setting up the project, ensure you have the following:

- **Operating System**: Linux-based environment (e.g., Ubuntu 22.04, WSL2 on Windows)
- **Python Version**: Python 3.10 
- **Package Manager**: `pip` (ensure it's up-to-date with `pip install --upgrade pip`)

### Verify Python Version

To verify that you have the correct version of Python installed, run:

```bash
python3 --version
```

## Getting Started

1. Install Stable-Retro
- Open **Terminal** in your Linux environment
- Update packages
```bash
sudo apt-get update
```

-Install Pip
```bash
sudo apt-get install python3-pip
```

-Upgrade pip, setuptools, and wheel:
```bash
pip install --upgrade pip setuptools wheel
```

-Create a Virtual Environment:
### Navigate to your project directory and create a virtual environment:
```bash
python3 -m venv venv
```
and activate the venv
```bash
source venv/bin/activate
```

- Install Stable-retro
```bash
pip install stable-retro
```

2. Set Up the ROM File
- Copy the rom (.nes) file 
```bash
cp /PunchOut-RL/PunchOut.nes /PunchOut-RL/venv/lib/python3.10/site-packages/retro/data/stable/PunchOut-Nes/
cd /PunchOut-RL/venv/lib/python3.10/site-packages/retro/data/stable/PunchOut-Nes/
mv PunchOut.nes rom.nes
```
