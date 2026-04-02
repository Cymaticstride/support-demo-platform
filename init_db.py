from app import create_app
from app.extensions import db
from app.models import Article, Ticket

app = create_app()

with app.app_context():
    db.create_all()

    if Ticket.query.count() == 0:
        demo_tickets = [
            Ticket(
                title="用户无法登录系统",
                status="待处理",
                priority="高",
                owner="技术支持A"
            ),
            Ticket(
                title="客户反馈知识库搜索不到结果",
                status="处理中",
                priority="中",
                owner="技术支持B"
            ),
            Ticket(
                title="部署后首页显示 502",
                status="已解决",
                priority="高",
                owner="实施工程师"
            )
        ]
        db.session.add_all(demo_tickets)

    if Article.query.count() == 0:
        demo_articles = [
            Article(
                title="如何初始化部署环境",
                category="部署指南",
                summary="介绍项目启动前需要检查的 Python、MySQL 和 Docker 环境。",
                content="这里是部署指南的正文内容。"
            ),
            Article(
                title="Nginx 反向代理常见报错排查",
                category="故障处理",
                summary="整理 502、404、端口不通等常见问题的排查思路。",
                content="这里是故障排查文章的正文内容。"
            ),
            Article(
                title="工单处理标准流程",
                category="支持流程",
                summary="说明从接单、定位、处理到回访的基本步骤。",
                content="这里是工单处理流程正文内容。"
            )
        ]
        db.session.add_all(demo_articles)

    db.session.commit()

    print("数据库初始化完成，演示数据已写入。")