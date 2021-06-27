# Web calulator
### Simple web application on fastapi

## Requirements
Python 3.8+

## Installation
* <b>Download project</b>
```console
$ git clone https://github.com/goody-py/calculator.git
```
* <b>Create virtual environment</b>
```console
$ python3 -m venv env
```
* <b> Activate virtual environment</b>
```console
$ . env/bin/activate
```
* <b>Install dependencies</b>
```console
$ pip install -r requirements.txt

---> 100%
```
## Run app
* <b>Run unicorn server</b>
```console
$ uvicorn calculator:calculator --reload --host 0.0.0.0 --port 8000

```
* <b>Run api tests </b>
```console
$ pytest .
```
## Finally
[Open link](http://localhost:8000/)
