@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating environment and installing packages...
call venv\Scripts\activate
pip install customtkinter pillow

echo Setup complete!
pause