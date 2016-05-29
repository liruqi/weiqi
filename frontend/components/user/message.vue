<template>
    <div class="room-page">
        <div class="flex-column" v-if="room">
            <template v-if="room">
                <qi-room-logs :room_id="room.room_id" :title="room.other_display"></qi-room-logs>
            </template>
            <template v-else>
                <div id="page-load-spinner">
                    <i class="fa fa-spinner fa-5x fa-spin"></i>
                </div>
            </template>
        </div>
    </div>
</template>

<script>
    import { load_direct_room } from '../../vuex/actions';

    export default {
        mixins: [require('./../../mixins/title.vue')],

        vuex: {
            getters: {
                direct_rooms: function(state) { return state.direct_rooms }
            },
            actions: {
                load_direct_room
            }
        },

        route: {
            canReuse: false
        },

        data() {
            return {
                room_id: null
            }
        },

        computed: {
            window_title() {
                if(!this.room) {
                    return '';
                }

                return this.room.other_display;
            },

            room() {
                return this.direct_rooms[this.$route.params.user_id];
            }
        },

        ready() {
            this.load_direct_room(this.$route.params.user_id);
        }
    }
</script>
