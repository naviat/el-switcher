# Acknowledgments
# client-switcher is branched from client - switcher written by Accidental - green: https: //github.com/accidental-green/client-switcher

#!/bin/bash
set -u

# enable  command completion
set -o history -o histexpand

python="python3"

abort() {
	printf "%s\n" "$1"
	exit 1
}

getc() {
	local save_state
	save_state=$(/bin/stty -g)
	/bin/stty raw -echo
	IFS= read -r -n 1 -d '' "$@"
	/bin/stty "$save_state"
}

exit_on_error() {
	exit_code=$1
	last_command=${@:2}
	if [ $exit_code -ne 0 ]; then
		echo >&2 "\"${last_command}\" command failed with exit code ${exit_code}."
		exit $exit_code
	fi
}

wait_for_user() {
	local c
	echo
	echo "Press RETURN to continue or any other key to abort"
	getc c
	# we test for \r and \n because some stuff does \r instead
	if ! [[ "$c" == $'\r' || "$c" == $'\n' ]]; then
		exit 1
	fi
}

shell_join() {
	local arg
	printf "%s" "$1"
	shift
	for arg in "$@"; do
		printf " "
		printf "%s" "${arg// /\ }"
	done
}

# string formatters
if [[ -t 1 ]]; then
	tty_escape() { printf "\033[%sm" "$1"; }
else
	tty_escape() { :; }
fi
tty_mkbold() { tty_escape "1;$1"; }
tty_underline="$(tty_escape "4;39")"
tty_blue="$(tty_mkbold 34)"
tty_red="$(tty_mkbold 31)"
tty_bold="$(tty_mkbold 39)"
tty_reset="$(tty_escape 0)"

ohai() {
	printf "${tty_blue}==>${tty_bold} %s${tty_reset}\n" "$(shell_join "$@")"
}

linux_install_pre() {
	sudo apt-get update
	sudo apt-get install --no-install-recommends --no-install-suggests -y curl git ccze
	exit_on_error $?
}

linux_install_python() {
	which $python
	if [[ $? != 0 ]]; then
		ohai "Installing python"
		sudo apt-get install --no-install-recommends --no-install-suggests -y $python
	else
		ohai "Updating python"
		sudo apt-get install --only-upgrade $python
	fi
	exit_on_error $?
	ohai "Installing python tools"
	sudo apt-get install --no-install-recommends --no-install-suggests -y $python-pip $python-tk $python-venv
	ohai "Creating venv"
	$python -m venv ~/.local --system-site-packages
	ohai "Installing pip requirements"
	~/.local/bin/pip install requests console-menu
	exit_on_error $?
}

linux_update_pip() {
	PYTHONPATH=$(which $python)
	ohai "You are using python@ $PYTHONPATH$"
	ohai "Installing python tools"
	$python -m pip install --upgrade pip
}

linux_install_client-switcher() {
	ohai "Cloning client-switcher into ~/git/el-switcher"
	mkdir -p ~/git/el-switcher
	git clone https://github.com/naviat/el-switcher.git ~/git/el-switcher/ 2>/dev/null || (
		cd ~/git/el-switcher
		git fetch origin master
		git checkout master
		git pull --ff-only
		git reset --hard
		git clean -xdf
	)
	ohai "Installing el-switcher"
	$python ~/git/el-switcher/client_switcher_cli.py
	exit_on_error $?
}

# Do install.
OS="$(uname)"
if [[ "$OS" == "Linux" ]]; then
	echo """
 ██████╗██╗     ██╗███████╗███╗   ██╗████████╗                
██╔════╝██║     ██║██╔════╝████╗  ██║╚══██╔══╝                
██║     ██║     ██║█████╗  ██╔██╗ ██║   ██║                   
██║     ██║     ██║██╔══╝  ██║╚██╗██║   ██║                   
╚██████╗███████╗██║███████╗██║ ╚████║   ██║                   
 ╚═════╝╚══════╝╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝                   
                                                              
███████╗██╗    ██╗██╗████████╗ ██████╗██╗  ██╗███████╗██████╗ 
██╔════╝██║    ██║██║╚══██╔══╝██╔════╝██║  ██║██╔════╝██╔══██╗
███████╗██║ █╗ ██║██║   ██║   ██║     ███████║█████╗  ██████╔╝
╚════██║██║███╗██║██║   ██║   ██║     ██╔══██║██╔══╝  ██╔══██╗
███████║╚███╔███╔╝██║   ██║   ╚██████╗██║  ██║███████╗██║  ██║
╚══════╝ ╚══╝╚══╝ ╚═╝   ╚═╝    ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                              
    """
	ohai "This script will install and switch your execution client:"
	echo "git"
	echo "curl"
	echo "ccze"
	echo "python3-tk"
	echo "python3-pip"
	echo "client-switcher"

	wait_for_user
	linux_install_pre
	linux_install_python
	linux_update_pip
	linux_install_client-switcher

	echo ""
	echo ""
	echo "######################################################################"
	echo "##                                                                  ##"
	echo "##                      CLIENT SWITCH COMPLETE                      ##"
	echo "##                                                                  ##"
	echo "######################################################################"
	echo ""
	echo ""
fi
