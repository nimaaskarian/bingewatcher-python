# bingewatcher-python
A simple command line tool to keep track of series and shows you watch. Written in python.
## Installation
- Clone this repo, make a `venv` and install the dependencies.
    ```
    git clone https://github.com/nimaaskarian/bingewatcher-python
    cd bingewatcher-python
    python3 -m venv .
    ./bin/pip install -r requirements.txt
    pwd
    ```
- Then copy the output of the last output of above commands, and add a `main.py` at the end of it.  
    For example `/home/user/bingewatcher-python` to `/home/user/bingewatcher-python/main.py`.  
- Add a `python3` to the beginning, resulting `python3 /home/user/bingewatcher-python/main.py`
- Then do `echo alias bw="python3 /home/user/bingewatcher-python/main.py" >> ~/.bashrc` (You may change `~/.bashrc` to your shells rc file. For example `~/.zshrc` for zsh)
-`source ~/.bashrc` (or any rc file you used)
- `bw -h` for help options.

