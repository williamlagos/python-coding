CC=gcc
CFLAGS=-c -Wall
CFLAGS+=$(shell python-config --cflags)
LDFLAGS+=$(shell python-config --ldflags)

all: module
	$(CC) $(CFLAGS) $(LDFLAGS) module.c -o module

clean:
	rm -rf *.o *.dSYM module