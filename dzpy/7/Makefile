.PHONY: all clean

all: main

clean:
	rm -rf main bin/*.o bin

CC      ?= gcc
CFLAGS  ?= -Wall -Wextra -Werror -ansi -pedantic
LDFLAGS ?= -lpthread

bin:
	mkdir -p bin

bin/main.o: src/main.c include/thread_pool.h src/thread_pool.c
	$(CC) $(CFLAGS) -c src/main.c -o bin/thread_pool.o
        
bin/thread_pool.o: src/thread_pool.c
	$(CC) $(CFLAGS) -c src/thread_pool.c -o bin/thread_pool.o
          
main: bin bin/thread_pool.o bin/main.o
	$(CC) $(CFLAGS) -o main bin/thread_pool.o bin/main.o
