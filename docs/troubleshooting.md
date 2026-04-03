# 常见排障手册

本文档记录本项目在部署和访问时的常见问题与排查思路。

## 1. 页面打不开

先检查容器是否正常运行：

```bash
docker compose ps
```

再检查 Nginx 日志：

```bash
docker compose logs -f nginx
```

再直接请求本地入口：

```bash
curl -I http://127.0.0.1:8080
```

## 2. 数据库连接失败

查看数据库容器是否正常：

```bash
docker compose logs -f db
```

查看 Flask 容器日志：

```bash
docker compose logs -f web
```

进入数据库容器测试：

```bash
docker compose exec db mysql -uroot -p123456
```

## 3. Flask 容器启动失败

先看日志：

```bash
docker compose logs -f web
```

重点关注：

- 环境变量是否正确
- 数据库是否已就绪
- Python 依赖是否安装完整

## 4. Nginx 反向代理异常

检查配置语法：

```bash
docker compose exec nginx nginx -t
```

进入 Nginx 容器后直接访问 Flask：

```bash
docker compose exec nginx sh
wget -qO- http://web:5000/ | head
```

如果这里访问失败，说明问题通常不在浏览器，而在容器内部链路。

## 5. 端口占用

如果 `8080` 或 `3307` 已被本机其他程序占用，需要先检查监听情况：

```bash
ss -lntp
```

## 6. 一个常见排查顺序

建议排查顺序如下：

1. 先看容器是否运行
2. 再看日志
3. 再看端口是否监听
4. 再看 Nginx 能否访问 Flask
5. 最后检查数据库是否正常连接

## 7. 常用命令清单

```bash
docker compose ps
docker compose logs -f nginx
docker compose logs -f web
docker compose logs -f db
docker compose exec nginx nginx -t
ss -lntp
curl -I http://127.0.0.1:8080
```