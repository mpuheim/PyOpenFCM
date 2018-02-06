REM Full installation as Python package
@echo off
echo Changing directory to %~dp0
echo Installation started
echo ---------------------------
pushd %~dp0
pip install git+https://github.com/jsonpickle/jsonpickle.git
pip install --upgrade . 
echo ---------------------------
set /p=Done. Press ENTER to continue...
echo Changing directory back to default
popd
@echo on