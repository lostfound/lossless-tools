ifeq ("${PREFIX}", "")
PREFIX=/usr/local
endif

all:

install: all
	install -D apemustdie.py $(PREFIX)/lib/lossless-tools/apemustdie.py
	mkdir -m 0755 -p $(PREFIX)/bin
	ln -sf $(PREFIX)/lib/lossless-tools/apemustdie.py $(PREFIX)/bin/apemustdie

uninstall:
	rm -rf  $(PREFIX)/lib/lossless-tools $(PREFIX)/bin/apemustdie
