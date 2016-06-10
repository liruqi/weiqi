<script>
import { is_tab_visible } from '../visibility'
import { notify } from '../notify';

export default {
    vuex: {
        getters: {
            user: function(state) { return state.auth.user; },
            game_has_update: function (state) { return state.game_has_update; },
            open_games: function(state) { return state.open_games; }
        }
    },

    watch: {
        'game_updates': function (val, old) {
            if(!this.user.logged_in) {
                return;
            }

            if(is_tab_visible()) {
                return;
            }

            val = JSON.parse(val);
            old = JSON.parse(old);

            Object.keys(val).forEach(function(game_id) {
                if(!val[game_id] || val[game_id] == old[game_id]) {
                    return;
                }

                var game = this.open_games.find(function(game) {
                    return game.id == game_id;
                });

                if(this.user.user_id != game.black_user_id && this.user.user_id != game.white_user_id) {
                    return;
                }

                var other = (this.user.user_id == game.black_user_id ? game.white_display : game.black_display);

                notify(this.$t('notify.move_played', {opponent: other}));
            }.bind(this));
        }
    },

    computed: {
        game_updates() {
            return JSON.stringify(this.game_has_update);
        }
    }
}
</script>
