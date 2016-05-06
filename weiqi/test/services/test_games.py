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

import pytest
from weiqi.services import GameService
from weiqi.services.games import InvalidPlayerError, InvalidStageError
from weiqi.test.factories import GameFactory
from weiqi.board import BLACK, WHITE, EMPTY, PASS, RESIGN


def test_open(db, socket):
    game = GameFactory()

    svc = GameService(db, socket, game.black_user)
    svc.execute('open', {'game_id': game.id})

    assert socket.is_subscribed('game_data/'+str(game.id))
    assert socket.is_subscribed('game_update/'+str(game.id))

    assert socket.is_subscribed('room_message/'+str(game.room_id))
    assert socket.is_subscribed('room_user/'+str(game.room_id))
    assert socket.is_subscribed('room_user_left/'+str(game.room_id))


def test_move(db, socket):
    game = GameFactory()

    svc = GameService(db, socket, game.black_user)
    svc.execute('move', {'game_id': game.id, 'move': 30})

    assert game.board.at(30) == BLACK
    assert game.board.current == WHITE


def test_move_current_color(db, socket):
    game = GameFactory()
    svc = GameService(db, socket, game.white_user)

    with pytest.raises(InvalidPlayerError):
        svc.execute('move', {'game_id': game.id, 'move': 30})

    assert game.board.at(30) == EMPTY


def test_move_counting(db, socket):
    game = GameFactory(stage='counting')
    svc = GameService(db, socket, game.black_user)

    with pytest.raises(InvalidStageError):
        svc.execute('move', {'game_id': game.id, 'move': 30})

    assert game.board.at(30) == EMPTY


def test_move_finished(db, socket):
    game = GameFactory(stage='finished')
    svc = GameService(db, socket, game.black_user)

    with pytest.raises(InvalidStageError):
        svc.execute('move', {'game_id': game.id, 'move': 30})

    assert game.board.at(30) == EMPTY


def test_resign(db, socket):
    game = GameFactory(stage='counting')
    svc = GameService(db, socket, game.black_user)

    svc.execute('move', {'game_id': game.id, 'move': RESIGN})

    assert game.stage == 'finished'
    assert game.result == 'W+R'


def test_resign_counting(db, socket):
    game = GameFactory(stage='counting')
    svc = GameService(db, socket, game.black_user)

    svc.execute('move', {'game_id': game.id, 'move': RESIGN})

    assert game.stage == 'finished'


def test_game_finished(db, socket):
    game = GameFactory()
    socket.subscribe('game_finished')
    socket.subscribe('game_data/'+str(game.id))

    svc = GameService(db, socket, game.black_user)
    svc.execute('move', {'game_id': game.id, 'move': RESIGN})

    assert len(socket.sent_messages) == 2
    assert socket.sent_messages[0]['method'] == 'game_finished'
    assert socket.sent_messages[1]['method'] == 'game_data'


def test_game_finished_rating_update(db, socket):
    game = GameFactory()
    socket.subscribe('rating_update/'+str(game.black_user_id))
    socket.subscribe('rating_update/'+str(game.white_user_id))

    svc = GameService(db, socket, game.black_user)
    svc.execute('move', {'game_id': game.id, 'move': RESIGN})

    assert len(socket.sent_messages) == 2
    assert socket.sent_messages[0]['method'] == 'rating_update'
    assert socket.sent_messages[1]['method'] == 'rating_update'


def test_stages_playing_counting(db, socket):
    game = GameFactory()
    svc = GameService(db, socket, game.black_user)

    svc.user = game.black_user
    svc.execute('move', {'game_id': game.id, 'move': PASS})
    assert game.stage == 'playing'

    svc.user = game.white_user
    svc.execute('move', {'game_id': game.id, 'move': PASS})
    assert game.stage == 'counting'


def test_toggle_marked_dead(db, socket):
    game = GameFactory(stage='counting')
    svc = GameService(db, socket, game.black_user)
    svc.user = game.black_user
    svc.socket.subscribe('game_update/'+str(game.id))

    game.board.play(30)
    game.apply_board_change()

    svc.execute('toggle_marked_dead', {'game_id': game.id, 'coord': 30})

    assert game.board.is_marked_dead(30)
    assert len(svc.socket.sent_messages) == 1
    assert svc.socket.sent_messages[0]['method'] == 'game_update'


def test_toggle_marked_dead_playing(db, socket):
    game = GameFactory(stage='playing')
    svc = GameService(db, socket, game.black_user)
    svc.user = game.black_user

    with pytest.raises(InvalidStageError):
        svc.execute('toggle_marked_dead', {'game_id': game.id, 'coord': 30})


def test_toggle_marked_dead_finished(db, socket):
    game = GameFactory(stage='finished')
    svc = GameService(db, socket, game.black_user)
    svc.user = game.black_user

    with pytest.raises(InvalidStageError):
        svc.execute('toggle_marked_dead', {'game_id': game.id, 'coord': 30})


def test_confirm_score(db, socket):
    game = GameFactory(stage='counting', result='B+1.5')
    svc = GameService(db, socket, game.black_user)
    svc.socket.subscribe('game_finished')
    svc.socket.subscribe('game_data/'+str(game.id))

    svc.user = game.black_user
    svc.execute('confirm_score', {'game_id': game.id, 'result': 'B+1.5'})

    assert game.result_black_confirmed == 'B+1.5'

    svc.user = game.white_user
    svc.execute('confirm_score', {'game_id': game.id, 'result': 'B+1.5'})

    assert game.result_white_confirmed == 'B+1.5'
    assert game.result == 'B+1.5'
    assert game.stage == 'finished'
    assert len(svc.socket.sent_messages) == 2
    assert svc.socket.sent_messages[0]['method'] == 'game_finished'
    assert svc.socket.sent_messages[1]['method'] == 'game_data'


def test_confirm_score_playing(db, socket):
    game = GameFactory(stage='playing', result='B+1.5')
    svc = GameService(db, socket, game.black_user)
    svc.user = game.black_user

    with pytest.raises(InvalidStageError):
        svc.execute('confirm_score', {'game_id': game.id, 'result': 'B+1.5'})


def test_confirm_score_finished(db, socket):
    game = GameFactory(stage='finished', result='B+1.5')
    svc = GameService(db, socket, game.black_user)
    svc.user = game.black_user

    with pytest.raises(InvalidStageError):
        svc.execute('confirm_score', {'game_id': game.id, 'result': 'B+1.5'})


def test_start_delay(db, socket):
    pytest.skip('not implemented')


def test_demo(db, socket):
    pytest.skip('not implemented')


def test_demo_control(db, socket):
    pytest.skip('not implemented')


def test_demo_resign(db, socket):
    pytest.skip('not implemented')


def test_demo_set_current_node(db, socket):
    pytest.skip('not implemented')


def test_demo_set_current_node_invalid(db, socket):
    pytest.skip('not implemented')
