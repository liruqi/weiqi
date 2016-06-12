<script>
import { is_tab_visible } from '../visibility'
import { notify } from '../notify';
import { add_event_listener } from '../events';

export default {
    vuex: {
        getters: {
            user: function(state) { return state.auth.user; }
        }
    },

    ready() {
        add_event_listener('game_update', this.handle_game_update);
    },

    methods: {
        handle_game_update(game) {
            if(!this.user.logged_in) {
                return;
            }

            if(is_tab_visible()) {
                return;
            }

            if(this.user.user_id != game.black_user_id && this.user.user_id != game.white_user_id) {
                return;
            }

            var other = (this.user.user_id == game.black_user_id ? game.white_display : game.black_display);
            notify(this.$t('notify.move_played', {opponent: other}));
        }
    }
}
</script>
