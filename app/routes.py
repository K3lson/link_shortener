from flask import Blueprint,request, render_template, redirect, url_for
from .models import db, URL

main = Blueprint('main', __name__)


@main.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        original_url = request.form['original_url']
        url = URL(original_url = original_url)
        db.session.add(url)
        db.session.commit()
        return render_template('result.html', short_url = url.short_url)
    
    return render_template('home.html')


@main.route('/<short_url>')
def redirect_to_url(short_url):
    link = URL.query.filter_by(short_url=short_url).first_or_404()
    return redirect(link.original_url)