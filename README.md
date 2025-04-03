# Helix

TODO: readme
## Setup
### Frontend Setup

Serve `index.html`, `style.css`, and `viewLayer.js` on
the Dolphin web server.

### API Setup

Do the following on a cub system.

Create a python virtual environment.

```bash
python -m venv .venv
```

Enter the virtual environment.
```
source .venv/bin/activate
```

Install dependencies from a requirements.txt

```bash
pip install -r requirements.txt
```

To activate a venv such that you are "in" that venv

```bash
source .venv/bin/activate
```

Set the global constant variable `apiAddress` in `viewLayer.js` to
the local IP of whichever cub you are running the API on.

## Known Issues
- There must be at least one quiz and therefore one course
for the frontend to render properly.