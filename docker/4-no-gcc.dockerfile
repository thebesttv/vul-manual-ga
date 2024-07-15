# 删除 gcc
RUN sudo apt-get remove --purge -y gcc >/dev/null && sudo apt-get autoremove -y >/dev/null

# 确保没有 gcc
RUN ! which gcc
