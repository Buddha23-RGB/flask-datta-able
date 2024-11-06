# -*- encoding: utf-8 -*-
from flask import Flask
from apps.home import blueprint as home_blueprint

app = Flask(__name__)
app.register_blueprint(home_blueprint, url_prefix='/home')

if __name__ == "__main__":
    app.run(debug=True)
