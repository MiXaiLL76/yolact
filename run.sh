#/bin/bash

# Очистка
./clean.sh

# Запуск контейнера
docker run --ipc=host --gpus all -it \
            -d -p 9999:9999 \
            -v $(pwd):/workspace \
            --name=yolact_research yolact/research