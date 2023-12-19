#!/usr/bin/env bash
# @Project      : AI @by PyCharm
# @Time         : 2023/12/15 08:41
# @Author       : betterme
# @Email        : 313303303@qq.com
# @Software     : PyCharm
# @Description  : https://mp.weixin.qq.com/s/bRzoTwL5j641ZPSAKlAAEg

# 指定更新nginx和redis容器名称
docker run -d \
  --name watchtower \
  --restart unless-stopped \
  -v /var/run/docker.sock:/var/run/docker.sock \
  containrrr/watchtower -c \
  nginx redis
