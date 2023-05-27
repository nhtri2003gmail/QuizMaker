import os
import platform

if platform.system() == "Linux":
    os.system('sudo apt install -y python3-tk')
os.system('pip install xlrd==1.2.0')
os.system('pip install docx2txt')