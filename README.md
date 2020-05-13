# BabyMonitor-RabbitMQ

## Tutorial
### Requirements:
- Python (Version >= 3.7)
- Virtualenv
- SQLite

### 1 - Create and activate the virtual enviroment:
Windows
```
virtualenv <nome_da_virtualenv>
<nome_da_virtualenv>\Scripts\activate
```

Ubuntu
```
python3 -m venv <nome_da_virtualenv>
source <nome_da_virtualenv>/bin/activate
```

### 2 - Install modules python:
```
pip install -r requirements.txt
```

### 2.1 - Python problem with install PyQt5?
Try:
```
pip install --upgrade pip
pip install PyQt5
```
Or try this link: https://stackoverflow.com/questions/59711301/install-pyqt5-5-14-1-on-linu

### 3 - Execute project:
```
python interface_devices.py
```
