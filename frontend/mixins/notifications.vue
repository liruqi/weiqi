<script>
import { notify } from '../notify';
import { add_event_listener } from '../events';

export default {
    vuex: {
        getters: {
            user: function(state) { return state.auth.user; },
            challenges: function(state) { return state.challenges; },
            rooms: function(state) { return state.rooms; }
        }
    },

    ready() {
        add_event_listener('game_update', this.handle_game_update);
        add_event_listener('room_message', this.handle_room_message);
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
                    var msg = this.$t('notify.challenge', {opponent: challenge.owner_display});
                    notify(msg, function() {
                        this.$router.go({name: 'challenge', params: {challenge_id: challenge.id}});
                    }.bind(this));
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
            var msg = this.$t('notify.move_played', {opponent: other});
            notify(msg, function() {
                this.$router.go({name: 'game', params: {game_id: game.id}});
            }.bind(this));
        },

        handle_room_message(msg) {
            if(!this.user.logged_in) {
                return;
            }

            var room = this.rooms.find(function(room) {
                return room.id == msg.room_id;
            });

            if(!room) {
                return;
            }

            var notify_msg = msg.user_display + ': ' + msg.message;
            var mentioned = msg.message.toLowerCase().indexOf(this.user.user_display.toLowerCase()) !== -1;

            if(room.type == 'main' && mentioned) {
                notify(notify_msg, function() {
                    this.$router.go({name: 'room', params: {room_id: room.id}});
                }.bind(this));
            } else if(room.type == 'direct') {
                notify(notify_msg, function() {
                    this.$router.go({name: 'user_message', params: {user_id: msg.user_id}});
                }.bind(this));
            }
        }
    }
}
</script>
