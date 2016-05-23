<script>
import { add_visibility_event_listener, is_tab_visible } from '../visibility'
import { clear_room_update } from '../vuex/actions';

export default {
    vuex: {
        getters: {
            room_has_update: function(state) { return state.room_has_update; }
        },
        actions: {
            clear_room_update
        }
    },

    ready() {
        add_visibility_event_listener(this.visibility_change);
    },

    watch: {
        'has_room_updates': function() {
            this.clear_current_room_updates();
        },

        '$route.params.user_id': function() {
            this.clear_current_room_updates();
        }
    },

    computed: {
        has_room_updates() {
            var room = Object.keys(this.room_has_update).find(function(room_id) {
                return this.room_has_update[room_id];
            }.bind(this));

            return !!room;
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
                this.clear_room_update(this.$route.params.user_id);
            }
        }
    }
}
</script>