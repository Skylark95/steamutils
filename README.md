# Steam Python Scripts

## Prerequisites
- Python 3
- MacOS, Linux, WSL, or Git Bash
- Steam account and Steam API Key

## Installation
- Clone the repository:
    ```
    git clone https://github.com/Skylark95/steam-python-scripts.git && cd steam-python-scripts
    ```
- Create and activate python virtual environment
    ```
    python3 -m venv .venv && source ./venv/bin/activate
    ```
- Install dependencies:
    ```
    pip install -r requirements.txt
    ```
- Create `.env` in root of project directory with the following content:
    ```
    STEAM_API_KEY={replace with your steam api key}
    STEAM_ID={replace with your steam id}
    ```

## Modules

### steam_games
Print a list of owned steam games to the terminal.

```
./venv/bin/python3 steam_games.py
```