<script>
import { add_visibility_event_listener, is_tab_visible } from '../visibility'
import { clear_room_update } from '../vuex/actions';

export default {
    vuex: {
        getters: {
            room_has_update: function(state) { return state.room_has_update; },
            direct_rooms: function(state) { return state.direct_rooms; },
            open_games: function(state) { return state.open_games }
        },
        actions: {
            clear_room_update
        }
    },

    ready() {
        add_visibility_event_listener(this.visibility_change);
    },

    watch: {
        'room_has_update': {
            handler: function () {
                this.clear_current_room_updates();
            },
            deep: true
        },

        '$route': {
            handler: function() {
                this.clear_current_room_updates();
            },
            deep: true
        }
    },

    methods: {
        visibility_change() {
            if(is_tab_visible()) {
                this.clear_current_room_updates();
            }
        },

        clear_current_room_updates() {
            if(this.$route.name == 'room' && is_tab_visible()) {
                this.clear_room_update(this.$route.params.room_id);
            }

            if(this.$route.name == 'user_message' && is_tab_visible()) {
                var direct = this.direct_rooms[this.$route.params.user_id];
                if(direct) {
                    this.clear_room_update(direct.room_id);
                }
            }

            if(this.$route.name == 'game' && is_tab_visible()) {
                var game_id = this.$route.params.game_id;
                var game = this.open_games[game_id] || {};

                if(game.room_id) {
                    this.clear_room_update(game.room_id);
                }
            }
        }
    }
}
</script>