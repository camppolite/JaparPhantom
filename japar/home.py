from flask import Blueprint, render_template
from japar.db import get_db

bp = Blueprint('home', __name__)


@bp.route('/')
def index():
    """Show the article, most recent first."""
    with get_db().cursor() as cursor:
        cursor.execute(
            'SELECT au.id, auth_inf_uid, auth_name, wcount, artcount, enjoy'
            ' FROM auth_inf au JOIN thedoor ON au.auth_inf_uid = thedoor.id'
        )
        auth_inf = cursor.fetchall()

        cursor.execute(
            'SELECT ar.id, art_inf_uid, created, arttitle, bcontexts, tag, rcount, awesome, oppose'
            ' FROM art_inf ar'
        )
        art_inf = cursor.fetchall()

    return render_template("home.html")
