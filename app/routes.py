from flask import Blueprint, render_template

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html")


@main_bp.route("/tickets")
def tickets():
    demo_tickets = [
        {
            "id": 1,
            "title": "用户无法登录系统",
            "status": "待处理",
            "priority": "高",
            "owner": "技术支持A"
        },
        {
            "id": 2,
            "title": "客户反馈知识库搜索不到结果",
            "status": "处理中",
            "priority": "中",
            "owner": "技术支持B"
        },
        {
            "id": 3,
            "title": "部署后首页显示 502",
            "status": "已解决",
            "priority": "高",
            "owner": "实施工程师"
        }
    ]
    return render_template("tickets.html", tickets=demo_tickets)


@main_bp.route("/kb")
def kb():
    articles = [
        {
            "title": "如何初始化部署环境",
            "category": "部署指南",
            "summary": "介绍项目启动前需要检查的 Python、MySQL 和 Docker 环境。"
        },
        {
            "title": "Nginx 反向代理常见报错排查",
            "category": "故障处理",
            "summary": "整理 502、404、端口不通等常见问题的排查思路。"
        },
        {
            "title": "工单处理标准流程",
            "category": "支持流程",
            "summary": "说明从接单、定位、处理到回访的基本步骤。"
        }
    ]
    return render_template("kb.html", articles=articles)