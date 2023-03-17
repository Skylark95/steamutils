# steamutils
CLI for interacting with the Steam API

## Prerequisites
- Python 3
- Steam API Key

## Installation
- Clone the repository:
    ```
    git clone https://github.com/Skylark95/steamutils.git && cd steamutils
    ```
- Create and activate python virtual environment
    ```
    python3 -m venv .venv && source ./venv/bin/activate
    ```
- Install dependencies:
    ```
    pip install -r requirements.txt
    ```
- Install CLI script
    ```
    pip install --editable .
    ```
## Usage
```
Usage: steamutils [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  apikey  Set the Steam API Key.
  games   Lookup owned steam games.
  user    Lookup SteamID by username.
```