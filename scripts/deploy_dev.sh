#!/bin/bash
# ©2022 TickSy
# TickSy development environment deployment script
# Prerequisites
# Ubuntu 20.04+

PARENT_DIR="$(dirname "$(pwd)")"
PYTHON3_PACK_NAME="python3"
APT_PACKAGES="python3-venv python3-dev python3-pip mariadb-server libmariadb-dev-compat libmariadb-dev libssl-dev"

function install_apt_package(){
  echo "Checking installation of $1"
  if [ "$(dpkg-query -W -f='${Status}' "$1" 2>/dev/null | grep -c "ok installed")" -eq 0 ]; then
    apt-get install "$1";
  else
    echo "Package $1 already installed on the system!";
  fi
}

function generate_python_venv(){
  echo "Generating Python virtual environment"
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
  echo "Resolving pip dependencies from requirements.txt"
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
  echo "Installing required apt packages"
  for PACKAGE in $APT_PACKAGES; do
    install_apt_package "$PACKAGE"
  done
}

function my_sql_secure(){
  echo "Running My SQL secure installation script";
  sudo mysql_secure_installation;
}

function configure_database(){
  echo "Configuring MariaDB development database and development user";
  sudo mariadb -e "CREATE OR REPLACE USER ticksy_dev@localhost IDENTIFIED BY 'dev';";
  if [ $? ]; then
    echo "TickSy development user created successfully!";
  else
    echo "Failed to create TickSy development user!";
    exit 1;
  fi
  sudo mariadb -e "DROP DATABASE IF EXISTS ticksy_cmdb;";
  sudo mariadb -e "CREATE OR REPLACE DATABASE ticksy_cmdb;";
  if [ $? ]; then
    echo "TickSy development database created successfully!";
  else
    echo "Failed to create TickSy development database!";
    exit 1;
  fi
  sudo mariadb -e "GRANT ALL ON ticksy_cmdb.* TO ticksy_dev@localhost IDENTIFIED BY 'dev' WITH GRANT OPTION;";
  if [ $? ]; then
    echo "TickSy development user granted development database permissions!";
  else
    echo "Failed to grant TickSy development user development database permissions!";
    exit 1;
  fi
  sudo mariadb -e "FLUSH PRIVILEGES;";
}

if [ "$EUID" -ne 0 ]
  then echo "Please run the script as root!"
  exit
fi

echo;
echo "TickSy development environment deployment script";
echo;
echo "WARNING!!!";
echo "This script will drop and reset the TickSy database! Continue at your own RISK!!!";
echo "Script only to be used for development/testing purposes, not for production deployment!";
echo;

while true
do
    read -r -p 'Do you want to start the setup process? Y(y)/N(n) ' choice
    case "$choice" in
      n|N) break;;
      y|Y) echo; install_apt_dependencies; echo; generate_python_venv; echo; install_pip_dependencies; echo; configure_database; break;; #my_sql_secure; break;;
      *) echo 'Response not valid';;
    esac
done

echo;
echo "TickSy development deployment completed successfully!";
