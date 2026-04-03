# 部署说明

本文档说明如何在本地通过 Docker Compose 启动本项目。

## 一、环境要求

本项目默认在以下环境中运行：

- Docker
- Docker Compose

## 二、启动步骤

进入项目根目录后执行：

```bash
docker compose up -d --build
```

首次启动时会完成以下动作：

1. 拉取 MySQL 和 Nginx 镜像
2. 构建 Flask 应用镜像
3. 启动 MySQL 容器
4. 启动 Flask 容器
5. 启动 Nginx 容器
6. 自动初始化数据库并写入演示数据

## 三、访问入口

浏览器访问：

```text
http://127.0.0.1:8080
```

## 四、常用命令

查看容器状态：

```bash
docker compose ps
```

查看日志：

```bash
docker compose logs -f nginx
docker compose logs -f web
docker compose logs -f db
```

停止服务：

```bash
docker compose stop
```

重新启动：

```bash
docker compose start
```

关闭并删除容器：

```bash
docker compose down
```

关闭并删除容器及数据卷：

```bash
docker compose down -v
```

## 五、数据库连接

若使用 DBeaver 连接本地数据库，可使用以下信息：

- Host: `127.0.0.1`
- Port: `3307`
- User: `root`
- Password: `123456`
- Database: `support_demo`

## 六、访问链路说明

项目的访问链路为：

**浏览器 -> Nginx -> Flask -> MySQL**

其中：

- Nginx 负责反向代理
- Flask 负责页面与业务逻辑
- MySQL 负责数据存储