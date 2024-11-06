# -*- encoding: utf-8 -*-
import os
from flask import current_app as app
from flask_login import current_user, login_user
from flask_dance.consumer import oauth_authorized
from flask_dance.contrib.github import github, make_github_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from apps.config import Config
from .models import Users, db, OAuth
from flask import redirect, url_for, flash

github_blueprint = make_github_blueprint(
    client_id=Config.GITHUB_ID,
    client_secret=Config.GITHUB_SECRET,
    scope='user',
    storage=SQLAlchemyStorage(
        OAuth,
        db.session,
        user=current_user,
        user_required=False,
    ),
)


class OAuth(OAuthConsumerMixin, db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey(Users.id))
    user = db.relationship(Users)


@oauth_authorized.connect_via(github_blueprint)
def github_logged_in(blueprint, token):
    info = github.get("/user")

    if info.ok:
        account_info = info.json()
        username = account_info["login"]

        query = Users.query.filter_by(oauth_github=username)
        try:
            user = query.one()
            login_user(user)
        except NoResultFound:
            # Save to db
            user = Users()
            user.username = '(gh)' + username
            user.oauth_github = username

            # Save current user
            db.session.add(user)
            db.session.commit()

            login_user(user)
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while logging in with GitHub.', 'error')
            return redirect(url_for('home.index'))

    return redirect(url_for('home.index'))
