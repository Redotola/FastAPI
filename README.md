# FastAPI
Curso FastAPI en Python

# Environment
python3 -m venv env

# Activate environment
source env/bin/activate

# Activate host
pip install uvicorn
uvicorn main:app 
uvicorn main:app --reload

# Select port and create a host
uvicorn main:app --reload --port (port number)
uvicorn main:app --port (port number) --host (host port number)

# Path to the documentation directory
(Path)/docs

