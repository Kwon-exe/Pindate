# PinDate

This is PinDate, a data-driven platform for discovering and sharing date spots — think Beli, but for any type of venue (restaurants, bars, arcades, hiking trails, etc.). Users can search by vibe or category, view venues and their info, save venues to personal lists, and leave reviews. Owners can apply to have their venues added and create posts for users to see.
Built for CS3200 by The Itinerary Engineers using Streamlit, Flask, and MySQL.

## Contributors:
* Alex Mohammed
* William Harnett
* Wyatt Bruch
* Jason Chao
* Kwon Lok Young

## How To Run Our Site

### Prerequisites

- A GitHub Account
- A terminal-based git client or GUI Git client such as GitHub Desktop or the Git plugin for VSCode.
- A distribution of Python running on your laptop.
- VSCode with the Python Plugin installed
- Docker Desktop

### Steps
1. Create a new Python environment in Python 3.11. 
   * If you're using the regular Python distribution: 
   ```bash
   python -m venv .env –python=python3.11
   ```
   * If you're using Anaconda or Miniconda:
   ```bash
   conda create -n db-proj python=3.11
   ```

2. Install the Python dependencies listed in `api/requirements.txt` and `app/src/requirements.txt` into your local Python environment.
```bash
cd api
pip install -r requirements.txt
cd ../app/src
pip install -r requirements.txt
```

3. Clone the repository into your local machine.
```bash
git clone git@github.com:Kwon-exe/Pindate.git
```

4. Open the repository in VSCode.

5. Navigate to the `/api` folder and set up the `.env` file based on the `.env.template` file.
   1. Make a copy of the `.env.template` file and name it `.env`. 
   1. Open the new `.env` file. 
   1. On the last line, delete the `<...>` placeholder text, and put a password. Don't reuse any passwords you use for any other services (email, etc.) 

6. Start the Docker containers.
```bash
docker compose up -d
```

7. In your browser, input this URL to open the site.
```
http://localhost:8501/
```

8. You're in PinDate!