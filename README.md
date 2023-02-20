# Slice of Life Server App
## Development Instructions
1. Clone the repository to your computer:
```
git clone https://github.com/slicersoflife/server.git
cd server
```
2. Setup Python virtual environments with [virtualenv-wrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html).
3. Make a virtual environment for this project:

```
mkvirtualenv slice-of-life-server
```
4. Install the required dependencies:
```
pip install -r requirements.txt
```
5. Obtain the `.env` file with the required variables.
6. Run the server: `./run_gunicorn.sh` OR `python flask_handler.py`.
