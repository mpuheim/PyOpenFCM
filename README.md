# PyOpenFCM  
Python Open Fuzzy Cognitive Maps Library (with Web API)  

Depedencies:  
- flask, jsonpickle  

Fast install & run Web API on Windows:  
- download & extract ZIP archive  
- run 'setup.bat' as admin  
- run 'fcmapi_service.bat' from CMD  
- open browser on http://localhost:5000/  

Install on other systems:
- download & extract ZIP archive  
- run elevated CMD in extracted directory  
- pip install git+https://github.com/jsonpickle/jsonpickle.git   
- pip install .  

Usage of library:  
- from fcmlib import FCM  
- map=FCM()  

Exemplary usage in script:  
- example.py  

Usage of Web API:  
- set FLASK_APP=fcmapi_app.py  
- set FLASK_DEBUG=0  
- flask run --host=0.0.0.0  