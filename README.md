# BabyMonitor-RabbitMQ

## Tutorial
### Requirements:
- Python (Version >= 3.7)
- Virtualenv
- SQLite
- Docker

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

#### 2.1 - Problem installing PyQt5?
Try:
```
pip install --upgrade pip
pip install PyQt5
```
Or try this link: https://stackoverflow.com/questions/59711301/install-pyqt5-5-14-1-on-linu

### 3 - Execute the project:
#### 3.1 - Run Broker (Docker and RabbitMQ) 
```
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```
#### 3.2 - Execute System BabyMonitor
```
python interface_devices.py
```

### Observation:
The broker and System BabyMonitor run in differents terminals.


