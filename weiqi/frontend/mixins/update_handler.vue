<script>
import { add_visibility_event_listener, is_tab_visible } from '../visibility'
import { clear_room_update } from '../vuex/actions';

export default {
    vuex: {
        getters: {
            rooms: function(state) { return state.rooms },
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

        '$route.params.room_id': function() {
            this.clear_current_room_updates();
        }
    },

    computed: {
        has_room_updates() {
            var room = Object.keys(this.room_has_update).find(function(room_id) {
                if(!this.room_has_update[room_id]) {
                    return false;
                }

                var room = this.rooms.find(function(room) {
                    return room.id == room_id;
                });

                return !room || room.type != 'game';
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
        }
    }
}
</script>