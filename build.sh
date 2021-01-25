#/bin/bash

# Очистка
./clean.sh

# Собрать родительский контейнер
DOCKER_BUILDKIT=1 docker build -t yolact/research .
