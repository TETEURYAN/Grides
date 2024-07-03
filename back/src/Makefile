CC = g++
CFLAGS = -std=c++11 -Wall
TARGET_C++ = example.cpp
TARGET_PY = main.py
SRC_C++_FILE = ../app/$(TARGET_C++)
SRC_PY_FILE = ../app/$(TARGET_PY)
EX1_FILE = ../tests/ex01.in
MAIN_FILE = main
FLAGS = -lilocplex -lcplex -lm -lpthread
LIBSIN =  -I/home/teteu/apps/cplex/cplex/include
LIBSOUT = -L/home/teteu/apps/cplex/cplex/lib64  
TESTS = ../tests

all: execPy

example: $(SRC_C++_FILE)
	@echo "Compilando $(TARGET_C++) para $(SRC_C++_FILE)"
	$(CC) $(CFLAGS) $(LIBSIN) $(SRC_C++_FILE) $(LIBSOUT) -o main $(FLAGS)

execC:
	./main < $(EX1_FILE)

execPy:
	@echo "Executando $(SRC_PY_FILE) com as entradas de $(TESTS)"
	python3 $(SRC_PY_FILE)

clean:
	rm -f $(MAIN_FILE)
