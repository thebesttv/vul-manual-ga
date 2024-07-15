FROM ubuntu:22.04

# 添加用户 thebesttv
RUN apt-get update >/dev/null && apt-get install -y sudo >/dev/null && \
    groupadd wheel && \
    useradd -m -G wheel -s /bin/bash thebesttv && \
    echo '%wheel ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers

# 安装必要的编译依赖
# 尽量不要用 gcc，改用 clang
RUN apt-get update >/dev/null && apt-get install -y >/dev/null \
    git jq \
    llvm clang clang-tools \
    autoconf automake cmake

USER thebesttv
WORKDIR /home/thebesttv
