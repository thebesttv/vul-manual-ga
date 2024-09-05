# '#++++++++++++++++++' 开头的行是可以修改的
# 最终要求：成功编译，并且 /home/thebesttv/项目名称/cc.json 是非空的

#++++++++++++++++++
# 项目名称和版本
#    项目会在 /home/thebesttv/${TBT_PACKAGE_NAME}
#    然后 checkout 到对应版本
ENV TBT_PACKAGE_NAME=FFmpeg
ENV TBT_PACKAGE_VERSION=8b152c355f6c52ddf5b5b1c6a90bcfb8468fe8d3
ENV TBT_PACKAGE_URL=https://github.com/FFmpeg/FFmpeg.git

#++++++++++++++++++
# 下载项目并checkout到固定版本
# 如果不是 Git 项目的话，需要修改
RUN git clone ${TBT_PACKAGE_URL} && \
    cd ${TBT_PACKAGE_NAME} && \
    git checkout ${TBT_PACKAGE_VERSION}

# 修改当前目录
WORKDIR /home/thebesttv/${TBT_PACKAGE_NAME}

#++++++++++++++++++
# 编译项目
RUN ./configure --cc=clang --disable-doc && \
    intercept-build make -w -j$(nproc)
