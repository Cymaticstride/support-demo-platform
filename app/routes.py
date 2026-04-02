from flask import Blueprint, flash, redirect, render_template, request, url_for

from .extensions import db
from .models import Article, Ticket

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    ticket_count = Ticket.query.count()
    article_count = Article.query.count()

    return render_template(
        "index.html",
        ticket_count=ticket_count,
        article_count=article_count
    )


@main_bp.route("/tickets")
def tickets():
    ticket_list = Ticket.query.order_by(Ticket.id.asc()).all()
    return render_template("tickets.html", tickets=ticket_list)


@main_bp.route("/tickets/new", methods=["GET", "POST"])
def new_ticket():
    form_data = {
        "title": "",
        "status": "待处理",
        "priority": "中",
        "owner": ""
    }

    if request.method == "POST":
        form_data["title"] = request.form.get("title", "").strip()
        form_data["status"] = request.form.get("status", "待处理").strip()
        form_data["priority"] = request.form.get("priority", "中").strip()
        form_data["owner"] = request.form.get("owner", "").strip()

        if not form_data["title"]:
            flash("工单标题不能为空。")
            return render_template("new_ticket.html", form_data=form_data)

        if not form_data["owner"]:
            flash("负责人不能为空。")
            return render_template("new_ticket.html", form_data=form_data)

        new_ticket_obj = Ticket(
            title=form_data["title"],
            status=form_data["status"],
            priority=form_data["priority"],
            owner=form_data["owner"]
        )

        db.session.add(new_ticket_obj)
        db.session.commit()

        flash("工单创建成功。")
        return redirect(url_for("main.tickets"))

    return render_template("new_ticket.html", form_data=form_data)


@main_bp.route("/kb")
def kb():
    article_list = Article.query.order_by(Article.id.asc()).all()
    return render_template("kb.html", articles=article_list)