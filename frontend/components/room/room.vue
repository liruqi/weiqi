<template>
    <div class="room-page">
        <section class="content">
            <div class="row">
                <div class="flex-column col-sm-9 col-lg-10">
                    <qi-room-logs :room-id="$route.params.roomID"></qi-room-logs>
                </div>
                <div class="flex-column col-sm-3 col-lg-2">
                    <qi-room-users :room-id="$route.params.roomID"></qi-room-users>
                </div>
            </div>
        </section>
    </div>
</template>

<script>
    export default {
        mixins: [require('./../../mixins/title.vue')],

        vuex: {
            getters: {
                rooms: function(state) { return state.rooms }
            }
        },

        computed: {
            windowTitle() {
                return this.room.Name;
            },

            room() {
                return this.rooms.find(room => { return room.ID == this.$route.params.roomID; }) || {};
            }
        }
    }
</script>