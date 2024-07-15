FROM ubuntu:22.04

# 添加用户 thebesttv
RUN apt-get update >/dev/null && apt-get install -y sudo >/dev/null && \
    groupadd wheel && \
    useradd -m -G wheel -s /bin/bash thebesttv && \
    echo '%wheel ALL=(ALL:ALL) NOPASSWD: ALL' >> /etc/sudoers

# 安装必要的编译依赖
# 尽量不要用 gcc，改用 clang
RUN apt-get update >/dev/null && apt-get install -y >/dev/null \
    git jq fuse ssh vim bat wget tmux \
    llvm clang clang-tools \
    autoconf automake cmake

# Create the privilege separation directory and fix permissions
RUN mkdir -p /run/sshd chmod 755 /run/sshd
# allow empty password
RUN passwd -d thebesttv && \
    sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config && \
    sed -i 's/#PermitEmptyPasswords no/PermitEmptyPasswords yes/g' /etc/ssh/sshd_config

RUN cd /usr/bin && \
    wget -O thebesttv \
        https://github.com/thebesttv/vul-llvm/releases/download/nightly/tool-x86_64.AppImage && \
    chmod +x thebesttv

USER thebesttv
WORKDIR /home/thebesttv

EXPOSE 22
CMD sudo /sbin/sshd ; bash
