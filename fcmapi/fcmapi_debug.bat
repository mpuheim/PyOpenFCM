echo Changing working directory to %~dp0
pushd %~dp0
set FLASK_APP=fcmapi_app.py&&set FLASK_DEBUG=1&&flask run
popd