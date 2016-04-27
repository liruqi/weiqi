<template>
    <div class="panel panel-default flex-column room-users">
        <table class="table table-hover table-striped table-condensed flex-auto">
            <thead>
                <tr>
                    <th>{{$t('roomUsers.username')}}</th>
                    <th>{{$t('roomUsers.rank')}}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users">
                    <td><qi-user-context :user-id="user.UserID"></qi-user-context></td>
                    <td><qi-rating-rank :rating="user.Rating"></qi-rating-rank></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import { loadRoomUsers } from '../../vuex/actions';

    export default {
        props: ['roomID'],

        vuex: {
            getters: {
                rooms: function(state) { return state.rooms; },
                roomUsers: function(state) { return state.roomUsers; }
            },
            actions: {
                loadRoomUsers
            }
        },

        computed: {
            users() {
                return this.roomUsers[this.roomID] || [];
            }
        },

        ready() {
            this.loadRoomUsers(this.roomID);
        }
    }
</script>