
TARGET_SCREEN_PY = app.py
SRC_PY_FILE = ./front/$(TARGET_SCREEN_PY)

all: execPy

execPy:
	@echo "Executando $(SRC_PY_FILE)"
	python3 $(SRC_PY_FILE)