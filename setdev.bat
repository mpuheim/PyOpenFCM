REM Setup development environment
@echo off
echo Changing directory to %~dp0
echo Installation started
echo ---------------------------
pushd %~dp0
pip install --upgrade . 
echo ---------------------------
echo Changing directory back to default
popd
@echo on