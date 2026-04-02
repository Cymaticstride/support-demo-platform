from flask import Blueprint, render_template

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


@main_bp.route("/kb")
def kb():
    article_list = Article.query.order_by(Article.id.asc()).all()
    return render_template("kb.html", articles=article_list)