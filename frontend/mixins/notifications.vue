<script>
import { notify } from '../notify';
import { add_event_listener } from '../events';

export default {
    vuex: {
        getters: {
            user: function(state) { return state.auth.user; },
            challenges: function(state) { return state.challenges; }
        }
    },

    ready() {
        add_event_listener('game_update', this.handle_game_update);
    },

    watch: {
        'challenges': function(new_val, old_val) {
            new_val.forEach(function(challenge) {
                if(challenge.owner_id == this.user.user_id) {
                    return;
                }

                var old_challenge = old_val.find(function(ch) {
                    return ch.id == challenge.id;
                });

                if(!old_challenge) {
                    notify(this.$t('notify.challenge', {opponent: challenge.owner_display}));
                }
            }.bind(this));
        }
    },

    methods: {
        handle_game_update(game) {
            if(!this.user.logged_in) {
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
