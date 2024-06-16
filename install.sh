#!/bin/bash

echo "╔══╣ Install: Ollama Python (STARTING) ╠══╗"


curl -fsSL https://ollama.com/install.sh | sh

python3 -m pip install ollama

sudo apt-get update
sudo apt install -y xterm

echo "╚══╣ Install: Ollama Python (FINISHED) ╠══╝"