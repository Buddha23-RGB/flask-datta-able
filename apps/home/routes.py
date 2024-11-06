# -*- encoding: utf-8 -*-
from apps.home import blueprint
from flask import render_template, request
from flask_login import login_required
from jinja2 import TemplateNotFound


@blueprint.route('/index')
@login_required
def index():
    sales_data = {
        "daily_sales": {"amount": 249.95, "percentage": 67, "progress": 50},
        "monthly_sales": {"amount": 2942.32, "percentage": 36, "progress": 35},
        "yearly_sales": {"amount": 12345.67, "percentage": 50, "progress": 50}
    }
    return render_template('home/index.html', segment='index', sales_data=sales_data)


@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
