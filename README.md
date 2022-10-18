# merc-parser
Hello,

This is a simple script to watch over a list of keywords on the japanese marketplace mercari. 
You will be emailed (or have logs) of the new items that come from time to time.

Just download the latest release for your operating system and edit config.yaml! 

Or, alternatively...

## Instructions

1. Install python (this was developed on 3.10.5)
2. Clone this repository `git clone https://github.com/Shaddox/merc-parser.git`
3. (Optional) Create a venv in the project directory `python3 -m venv .`
4. (Optional) Activate venv `<venv>\Scripts\activate.bat`
5. `pip3 install requirements.txt`
6. Copy (or rename) the example configuration file `cp config.yaml.example config.yaml`
7. Configure the script to your liking
8. Run it! `python3 main.py`
