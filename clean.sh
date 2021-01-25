#/bin/bash

# очистить все докеры без тегов или имен
while [ 1 ]
do
    none_tags=$(docker images | grep none | awk '{print $3}')
    if [ ${#none_tags} -gt 0 ]
    then
        docker rmi ${none_tags} --force
    else
        break
    fi
done

# очистить то, что уже завершено
exited=$(docker ps -qa --no-trunc --filter "status=exited")
if [ ${#exited} -gt 0 ]
then
    docker rm ${exited}
fi

# очистить то, что уже созданно, но не запущено.
exited=$(docker ps -qa --no-trunc --filter "status=created")
if [ ${#exited} -gt 0 ]
then
    docker rm ${exited}
fi

# Удалил временные файлы python
sudo rm -r $(find . -name "*__pycache__")
sudo rm -r $(find . -name "*.ipynb_checkpoints")