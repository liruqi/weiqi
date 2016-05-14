import {store, mutations, default_state} from '../vuex/store';

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
