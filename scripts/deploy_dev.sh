#!/bin/bash
# ©2022 TickSy
# TickSy development environment deployment script
# Prerequisites
# Ubuntu 20.04+

PARENT_DIR="$(dirname "$(pwd)")"
PYTHON3_PACK_NAME="python3"

function install_apt_package(){
  echo "Checking installation of $1"
  if [ "$(dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -c "ok installed")" -eq 0 ]; then
    apt-get install "$1";
  else
    echo "Package $1 already installed on the system!";
  fi
}

function generate_python_venv(){
    VENV_DIR="$PARENT_DIR/.venv"
    install_apt_package $PYTHON3_PACK_NAME;
    echo "Checking for Python venv existence";
    if [ -d "$VENV_DIR" ]; then
         echo "Found Python venv, skipping generation step!";
    else
        echo "No Python venv found, generating...";
        sudo -u "$SUDO_USER" python3 -m venv "$VENV_DIR";
    fi
    echo "Activating Python venv";
    if source "$VENV_DIR/bin/activate"; then
        echo "Python venv activated successfully!";
        pip3 list;
    else
        echo "Python venv failed to activate!";
        exit 1;
    fi
}

function install_pip_dependencies(){
  PIP_REQ_TXT="$PARENT_DIR/requirements.txt";
  if [ -f "$PIP_REQ_TXT" ]; then
    if pip3 install -r "$PIP_REQ_TXT"; then
      echo "Installed Python packages successfully!";
      pip3 list;
    else
      echo "Failed to install Python packages, aborting!";
      exit 1;
    fi
  else
    echo "Requirements.txt not found, aborting!";
    exit 1;
  fi
}

function install_apt_dependencies(){
    echo "";
}

if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root!"
  exit
fi

echo "TickSy development environment deployment script"

while true
do
    read -r -p 'Do you want to start the setup process? Y(y)/N(n) ' choice
    case "$choice" in
      n|N) break;;
      y|Y) generate_python_venv; install_apt_dependencies; install_pip_dependencies; break;;
      *) echo 'Response not valid';;
    esac
done