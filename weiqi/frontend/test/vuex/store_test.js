import {store, mutations, default_state} from '../../vuex/store';

describe('connection_data', function() {
    it('should set user info', function() {
        var state = default_state();
        
        mutations.MSG_CONNECTION_DATA(state, {
            user_id: 1,
            user_display: 'test'
        });

        expect(state.auth.user.user_id).toEqual(1);
        expect(state.auth.user.logged_in).toBeTruthy();
    });

    it('should not be logged in for guests', function() {
        var state = default_state();

        mutations.MSG_CONNECTION_DATA(state, {
            user_id: null
        });

        expect(state.auth.user.logged_in).toBeFalsy();
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
        
        expect(state.open_games[0].title).toEqual('title');
        expect(state.open_games[0].black_display).toEqual('black');
        expect(state.open_games[0].white_display).toEqual('white');
    });
});