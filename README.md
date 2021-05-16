# CITS5505 Agile Web Dev Group Project: Online Formative Assessment
Authors: Veronica Rao (23030918) and Aaron Norrish (21972015)

# Running the application
First navigate to the root directory and create a virtual environment:
```
python3 -m venv ./venv
```

then activate the environment and install the required packages:
```
source ./venv/bin/activate
pip install -r "requirements.txt"
```

migrate the database:
```
flask db upgrade
```

finally to run the application:
```
python3 main.py
```

# TODO 
turn off debugging in flaskenv file