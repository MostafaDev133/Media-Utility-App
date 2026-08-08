@echo off
echo Creating virtual environment...
python -m venv venv

echo Activating environment and installing packages...
call venv\Scripts\activate
pip install customtkinter pillow opencv-python

echo Setup complete!
pause