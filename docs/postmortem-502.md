# 502 故障复盘示例

## 一、故障现象

浏览器访问项目入口时，返回 502 Bad Gateway。

访问地址：

```text
http://127.0.0.1:8080
```

## 二、初步判断

502 通常说明：

- Nginx 已经收到请求
- 但 Nginx 无法正常从上游应用获取有效响应

本项目里，上游应用是 Flask 容器。

## 三、排查过程

### 1. 查看容器状态

```bash
docker compose ps
```

确认 `nginx`、`web`、`db` 三个服务是否正常运行。

### 2. 查看 Nginx 日志

```bash
docker compose logs -f nginx
```

观察是否存在 upstream 连接失败、host 解析失败、连接被拒绝等信息。

### 3. 查看 Flask 日志

```bash
docker compose logs -f web
```

确认 Flask 是否成功启动，是否因为数据库连接失败或代码报错而退出。

### 4. 检查 Nginx 配置

```bash
docker compose exec nginx nginx -t
```

确认语法无误。

### 5. 在 Nginx 容器内部直接访问 Flask

```bash
docker compose exec nginx sh
wget -qO- http://web:5000/ | head
```

如果这一步失败，说明问题在：

- `proxy_pass` 配置错误
- `web` 服务未正常启动
- 容器内部网络访问异常

## 四、定位结论

本次 502 的典型原因是：

- Nginx 配置中的上游地址错误
- Flask 容器未正常启动
- Flask 未监听正确地址
- 数据库未准备好导致 Flask 启动失败

## 五、修复动作

修复方向通常包括：

1. 检查 `proxy_pass` 是否指向正确的 `web:5000`
2. 检查 Flask 是否使用 `0.0.0.0` 监听
3. 检查数据库等待逻辑是否生效
4. 修改配置后重新启动服务

```bash
docker compose down
docker compose up -d --build
```

## 六、复盘结论

这类问题的核心不是“页面打不开”，而是：

**Nginx -> Flask 这一跳失败了。**

因此排查时不能只盯浏览器，必须进入容器网络内部验证代理链路。

## 七、经验沉淀

后续遇到类似问题，优先按下面顺序处理：

1. 看容器状态
2. 看 Nginx 日志
3. 看 Flask 日志
4. 测配置语法
5. 在 Nginx 容器内直接访问 Flask