<template>
    <div class="room-page">
        <div class="flex-column">
            <template v-if="room">
                <qi-room-logs :room-id="room.RoomID" :title="$route.params.userID"></qi-room-logs>
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
    import { loadDirectRoom } from '../../vuex/actions';

    export default {
        mixins: [require('./../../mixins/title.vue')],

        vuex: {
            getters: {
                directRooms: function(state) { return state.directRooms }
            },
            actions: {
                loadDirectRoom
            }
        },

        route: {
            canReuse: false
        },

        data() {
            return {
                roomID: null
            }
        },

        computed: {
            windowTitle() {
                return this.$route.params.userID;
            },

            room() {
                return this.directRooms[this.$route.params.userID];
            }
        },

        ready() {
            this.loadDirectRoom(this.$route.params.userID);
        }
    }
</script>
