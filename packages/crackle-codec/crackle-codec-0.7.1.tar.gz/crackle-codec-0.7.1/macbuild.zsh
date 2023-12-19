#!/bin/zsh

source ~/.zprofile

function compile_wheel {
	workon crackle$1
	pip install oldest-supported-numpy build -r requirements.txt
	python -m build
}

compile_wheel 38
compile_wheel 39
compile_wheel 310
compile_wheel 311
compile_wheel 312