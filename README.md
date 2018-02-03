# PyOpenFCM 
Python Open Fuzzy Cognitive Maps Library (with Web API) 

Depedencies:  
- flask, jsonpickle

Install depedencies:  
- pip install git+https://github.com/jsonpickle/jsonpickle.git 
- pip install flask 

Usage of library:  
- from lib.fcm import FCM  
- map=FCM()

Exemplary usage in script:  
- example.py  

Usage of Web API:  
- set FLASK_APP=api.py  
- set FLASK_DEBUG=0  
- flask run --host=0.0.0.0  

Now it is possible to run commands from browser as URLs.
