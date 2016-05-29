import { assert } from 'chai';
import {store, mutations, default_state} from '../../vuex/store';

describe('connection_data', function() {
    it('should set user info', function() {
        var state = default_state();
        
        mutations.MSG_CONNECTION_DATA(state, {
            user_id: 1,
            user_display: 'test'
        });

        assert.equal(state.auth.user.user_id, 1);
        assert.isOk(state.auth.user.logged_in);
    });

    it('should not be logged in for guests', function() {
        var state = default_state();

        mutations.MSG_CONNECTION_DATA(state, {
            user_id: null
        });

        assert.isNotOk(state.auth.user.logged_in);
    });
});

describe('game_info', function() {
    it('should set the game info', function() {
        var state = default_state();
        state.open_games.push({id: 1});
        
        mutations.MSG_GAME_INFO(state, {
            game_id: 1,
            title: 'title',
            black_display: 'black',
            white_display: 'white'
        });
        
        assert.equal(state.open_games[0].title, 'title');
        assert.equal(state.open_games[0].black_display, 'black');
        assert.equal(state.open_games[0].white_display, 'white');
    });
});