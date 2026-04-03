from flask import Blueprint, flash, redirect, render_template, request, url_for

from .extensions import db
from .models import Article, Ticket

main_bp = Blueprint("main", __name__)


def get_ticket_stats():
    return {
        "all": Ticket.query.count(),
        "pending": Ticket.query.filter_by(status="待处理").count(),
        "processing": Ticket.query.filter_by(status="处理中").count(),
        "resolved": Ticket.query.filter_by(status="已解决").count(),
    }


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
    status_filter = request.args.get("status", "全部").strip()
    valid_statuses = {"全部", "待处理", "处理中", "已解决"}

    if status_filter not in valid_statuses:
        status_filter = "全部"

    query = Ticket.query.order_by(Ticket.id.asc())

    if status_filter != "全部":
        query = query.filter(Ticket.status == status_filter)

    ticket_list = query.all()
    stats = get_ticket_stats()

    return render_template(
        "tickets.html",
        tickets=ticket_list,
        current_filter=status_filter,
        stats=stats
    )


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


@main_bp.route("/tickets/<int:ticket_id>/start", methods=["POST"])
def start_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.status == "待处理":
        ticket.status = "处理中"
        db.session.commit()
        flash(f"工单 #{ticket.id} 已进入“处理中”。")
    else:
        flash("只有“待处理”的工单才能开始处理。")

    return redirect(url_for("main.tickets"))


@main_bp.route("/tickets/<int:ticket_id>/resolve", methods=["POST"])
def resolve_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.status == "处理中":
        ticket.status = "已解决"
        db.session.commit()
        flash(f"工单 #{ticket.id} 已标记为“已解决”。")
    else:
        flash("只有“处理中”的工单才能标记为已解决。")

    return redirect(url_for("main.tickets"))


@main_bp.route("/tickets/<int:ticket_id>/reopen", methods=["POST"])
def reopen_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    if ticket.status == "已解决":
        ticket.status = "处理中"
        db.session.commit()
        flash(f"工单 #{ticket.id} 已重新打开。")
    else:
        flash("只有“已解决”的工单才能重新打开。")

    return redirect(url_for("main.tickets"))


@main_bp.route("/kb")
def kb():
    article_list = Article.query.order_by(Article.id.asc()).all()
    return render_template("kb.html", articles=article_list)