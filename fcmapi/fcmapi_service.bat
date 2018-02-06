echo Changing working directory to %~dp0
pushd %~dp0
set FLASK_APP=fcmapi_app.py&&set FLASK_DEBUG=0&&flask run --host=0.0.0.0
popd