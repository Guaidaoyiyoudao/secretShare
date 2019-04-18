from flask import (flash, g, redirect, render_template, request, session, url_for)
from werkzeug.security import check_password_hash, generate_password_hash
from . import main
from .. import login_manager
from flask_login import login_required

@main.route('/')
@login_required
def index():
    return render_template('index.html')
