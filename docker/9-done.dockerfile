# 确保 compile_commands.json 存在且是一个长度至少为1的数组
RUN if [ ! -f compile_commands.json ]; then \
        echo "compile_commands.json 不存在"; \
        exit 1; \
    fi && \
    if ! jq 'type == "array" and length > 0' compile_commands.json > /dev/null; then \
        echo "compile_commands.json 不是非空数组"; \
        exit 1; \
    fi
