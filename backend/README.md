# Set up and activate a virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

# Install the requirements
pip install -r requirements.txt

# Run Django Server 
python3 manage.py runserver
