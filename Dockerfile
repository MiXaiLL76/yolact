FROM nvidia/cuda:11.1.1-devel-ubuntu20.04
LABEL maintainer="mike.milos@yandex.ru"

# Делаем девайсы просматриваемыми
ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES compute,utility

# basic_config
WORKDIR /tmp
RUN DEBIAN_FRONTEND=noninteractive apt update
RUN DEBIAN_FRONTEND=noninteractive apt install \
                                        git curl \
                                        python3 python3-pip -y

# environment
RUN python3 -m pip install --no-cache-dir install Pillow
RUN python3 -m pip install --no-cache-dir install pycocotools

# OpenCV bug fix
RUN python3 -m pip install --no-cache-dir opencv-python
RUN DEBIAN_FRONTEND=noninteractive apt install libgl1-mesa-glx libglib2.0-0 -y

# torch
RUN python3 -m pip install --no-cache-dir torch
RUN python3 -m pip install --no-cache-dir torchvision

# Доп. либы
RUN python3 -m pip install --no-cache-dir pandas 
RUN python3 -m pip install --no-cache-dir numpy 
RUN python3 -m pip install --no-cache-dir matplotlib 
RUN python3 -m pip install --no-cache-dir imgaug 
RUN python3 -m pip install --no-cache-dir tqdm

WORKDIR /workspace


ENTRYPOINT ["bash"]



# Устанавливаем jupyterlab
RUN python3 -m pip install --no-cache-dir jupyterlab 

# jupyterlab работает со старой версией jedi
RUN python3 -m pip install --no-cache-dir jedi==0.17.2 idna==2.9 

# Настройка файла запуска jupyterlab
RUN sudo mkdir -m777 -p /app
ENV JUP_START "/usr/local/bin/jupyter-lab-starter"
COPY scripts/jupyter-lab-starter ${JUP_START}

ENV PORT 9999
# Открытие порта для jupyter
EXPOSE ${PORT}