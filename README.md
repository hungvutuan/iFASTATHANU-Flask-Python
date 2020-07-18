iFASTATHANU
===========
iFASTATHANU is an early-fire-alarming system, combining the strength of embedded system, aritifical intelligence and the ease of web application. It stands for "intelligent Fire Alarming SysTem with AI That Has A Nascent Ubiquity".

Author(s)
---------
Tuan Hung Vu - [GitHub](https://github.com/hungvutuan), [LinkedIn](https://www.linkedin.com/in/tuan-hung-vu-734349192/).

Requirements 
------------
Python 3.x is required to run this application. Download the latest version of Python 3.x [here](https://www.python.org/downloads/) and [configure the global environment variable PATH](https://geek-university.com/python/add-python-to-the-windows-path/) to your installation folder.
- Flask 1.1.x is required to run this application.

Flask installation (for Windows)
--------------------------
- Clone the codes from GitHub and extract the downloaded .ZIP file.
- Use Command Line (cmd) to download the latest version of Flask: 
```
pip install flask
```
- Add the Flask environment variable to PATH to use `flask`.
If you install Python at its default folder then use this command:
```
set PATH = C:\Users\YOUR-NAME\AppData\Local\Packages\PythonSoftwareFoundation.Python.3.x-YOUR-VERSION\LocalCache\local-packages\Python-YOUR-VERSION\Scripts
```

Running the back-end components
-------------------------------
- Install dependencies with:
```
pip install -r requirements.txt
```
- Establish the connection to MySQL database with the credentials in the code.
 - Then, navigate using `cd` to the extracted folder and use cmd to run:
```
set FLASK_APP=app.py
flask run
```

PEP 8 
-----
The syntax, indentation, naming scheme, layout, etc. of this application follow the [PEP 8](https://www.python.org/dev/peps/pep-0008/) style for Python code.
