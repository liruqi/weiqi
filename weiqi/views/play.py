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

from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from flask_socketio import emit
from weiqi import db
from weiqi.models import Room, RoomMessage, RoomUser, User, Automatch

bp = Blueprint('play', __name__)


@bp.route('/play/automatch', methods=['POST'])
@login_required
def automatch():
    preset = request.form['preset']
    max_hc = request.form['max_hc']

    return jsonify({})


@bp.route('/play/automatch/cancel', methods=['POST'])
@login_required
def cancel_automatch():
    pass


@bp.route('/play/upload-sgf', methods=['POST'])
@login_required
def upload_sgf():
    pass


@bp.route('/play/create-demo', methods=['POST'])
@login_required
def create_demo():
    pass


@bp.route('/play/challenge', methods=['POST'])
@login_required
def challenge():
    pass
