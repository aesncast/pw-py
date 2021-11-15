PROG=pw-py
IN=pw/__main__.py
EXE=dist/${PROG}

.PHONY: tests 

all: ${EXE}
	true

${EXE}: ${IN}
	pyinstaller --onefile --console "${IN}" -n ${PROG} \
	--exclude-module "PyQt5"
# TODO: optimize pyinstaller build

tests:
	PYTHONPATH=./:${PYTHONPATH} python3 ./tests/compatibility_tests.py

