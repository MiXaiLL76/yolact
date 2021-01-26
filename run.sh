#/bin/bash

# Очистка
./clean.sh

# Запуск контейнера
docker run --ipc=host --gpus all -it \
            -v $(pwd):/workspace \
            --name=yolact_research yolact/research