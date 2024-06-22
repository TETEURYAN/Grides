CC = g++
CFLAGS = -std=c++11 -Wall
TARGET = example.cpp
SRC_FILE = ../app/$(TARGET)
EX1_FILE = ../tests/ex01.in
MAIN_FILE = main

all: example exec clean

example: $(SRC_FILE)
	@echo "Compilando $(TARGET) para $(SRC_FILE)"
	$(CC) $(CFLAGS) $(SRC_FILE) -o main

exec:
	./main < $(EX1_FILE)

clean:
	rm -f $(MAIN_FILE)
