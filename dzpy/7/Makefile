.PHONY: all clean

all: pqsort

clean:
	rm -rf pqsort bin/*.o bin

CC      ?= gcc
CFLAGS  ?= -Wall -Wextra -Werror -ansi -pedantic

bin:
	mkdir -p bin

bin/main.o: src/main.c include/thread_pool.h src/thread_pool.c
	$(CC) $(CFLAGS) -c src/main.c -o bin/main.o -g
        
bin/thread_pool.o: src/thread_pool.c include/thread_pool.h
	$(CC) $(CFLAGS) -c src/thread_pool.c -o bin/thread_pool.o -g
          
pqsort: bin bin/thread_pool.o bin/main.o
	$(CC) $(CFLAGS) -o pqsort bin/thread_pool.o bin/main.o -lpthread -g
