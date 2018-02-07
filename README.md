# PyOpenFCM  
Python Open Fuzzy Cognitive Maps Library (with Web API)  

Depedencies:  
- Python 3.6  
- flask, jsonpickle  
- git  

Fast install & run Web API on Windows:  
- install GIT from https://git-scm.com/download/win
- download & extract repository ZIP archive  
- run 'setup.bat' as admin  
- run 'fcmapi/fcmapi_service.bat'    
- open browser on http://localhost:5000/  

Install on other systems:
- install GIT
- download & extract repository ZIP archive  
- run elevated CMD in extracted directory  
- pip install git+https://github.com/jsonpickle/jsonpickle.git   
- pip install .  

Usage of library in Python:  
- from fcmlib import FCM  
- map=FCM()  

Exemplary usage in script:  
- example.py  

Usage of Web API:  
- set FLASK_APP=fcmapi_app.py  
- set FLASK_DEBUG=0  
- flask run --host=0.0.0.0  