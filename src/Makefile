CC = g++
CFLAGS = -std=c++11 -Wall

all: example exec

example: example.cpp
	$(CC) $(CFLAGS) ./app/example.cpp -o main

exec:
	./main < output.in
