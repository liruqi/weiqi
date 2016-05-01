# weiqi.gs
# Copyright (C) 2016 Michael Bitzi
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Blueprint, request, abort, jsonify, redirect
from flask_login import login_user, logout_user, login_required
from weiqi import db
from weiqi.models import User, RoomUser, Room
from weiqi.rating import min_rating
from weiqi.glicko2 import Player

bp = Blueprint('auth', __name__)


@bp.route('/sign-up', methods=['POST'])
def sign_up():
    user = User(
        display=request.form['display'],
        email=request.form['email'])

    user.set_password(request.form['password'])
    _sign_up_rating(user, request.form['rank'])
    _sign_up_rooms(user)

    db.session.add(user)
    db.session.commit()

    login_user(user, remember=True)

    return jsonify({})


def _sign_up_rating(user, rank):
    rating = min_rating(rank)

    if rating < min_rating('20k') or rating > min_rating('3d'):
        abort(400)

    user.rating = rating
    user.rating_data = Player(rating)


def _sign_up_rooms(user):
    for room in Room.query.filter_by(type='main', is_default=True):
        ru = RoomUser(user=user, room=room)
        db.session.add(ru)


@bp.route('/email-exists', methods=['POST'])
def email_exists():
    exists = User.query.filter_by(email=request.form['email']).count() > 0
    return 'true' if exists else 'false'


@bp.route('/sign-in', methods=['POST'])
def sign_in():
    user = User.query.filter_by(email=request.form['email']).first()

    if not user or not user.check_password(request.form['password']):
        abort(401)

    login_user(user, remember=True)

    return jsonify({})


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
