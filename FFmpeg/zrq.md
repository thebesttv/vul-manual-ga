docker rm $(docker ps -aq)
docker rmi $(docker images -q)
m4 *.m4 > Dockerfile
docker build . -t thebesttv/vul-manual:*
docker run -it \
    --device /dev/fuse --cap-add SYS_ADMIN --security-opt apparmor:unconfined \
    -v $PWD:/data \
    -p 12345:22 \
    thebesttv/vul-manual:*
thebesttv --no-good-source --no-nodes --npe-fix /data/input.json