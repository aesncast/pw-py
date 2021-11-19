PROG=pw-py
IN=pw/__main__.py
EXE=dist/${PROG}
SOURCES=$(shell find pw -name "*.py")

MD5SUMS=md5sums.txt
SHA256SUMS=sha256sums.txt
SUMS=dist/${MD5SUMS} dist/${SHA256SUMS}

.PHONY: tests sign clean

all: ${EXE}
	true

${EXE}: ${SOURCES}
	python3 pw/config.py &&\
	pyinstaller --onefile --console "${IN}" -n ${PROG} \
	--exclude-module "PyQt5"
# TODO: optimize pyinstaller build

tests:
	PYTHONPATH=./:${PYTHONPATH} python3 ./tests/compatibility_tests.py

sign: ${SUMS}
	gpg --output dist/md5sums.txt.asc --detach-sign --armor dist/${MD5SUMS} &&\
	gpg --output dist/sha256sums.txt.asc --detach-sign --armor dist/${SHA256SUMS}

dist/${MD5SUMS}: ${EXE} ${EXE}.exe
	cd dist && md5sum ${PROG} ${PROG}.exe > ${MD5SUMS}

dist/${SHA256SUMS}: ${EXE} ${EXE}.exe
	cd dist && sha256sum ${PROG} ${PROG}.exe > ${SHA256SUMS}

clean:
	rm -rf ./build ./dist pw-py.spec pw_py.egg-info
