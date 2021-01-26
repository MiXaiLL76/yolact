#/bin/bash

# Очистка
./clean.sh

# Запуск контейнера
docker run --gpus all -it \
            -v $(pwd):/workspace \
            --name=yolact_research yolact/research