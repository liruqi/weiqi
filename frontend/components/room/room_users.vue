<template>
    <div class="panel panel-default room-users fixed-dropdowns">
        <table class="table table-hover table-striped table-condensed flex-auto">
            <thead>
                <tr>
                    <th>{{$t('room_users.username')}}</th>
                    <th>{{$t('room_users.rank')}}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="user in users">
                    <td><qi-user-context :user_id="user.user_id" :display="user.user_display"></qi-user-context></td>
                    <td><qi-rating-rank :rating="user.user_rating"></qi-rating-rank></td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import { load_room_users } from '../../vuex/actions';

    export default {
        props: ['room_id'],

        vuex: {
            getters: {
                rooms: function(state) { return state.rooms; },
                room_users: function(state) { return state.room_users; }
            },
            actions: {
                load_room_users
            }
        },

        computed: {
            users() {
                var users = this.room_users[this.room_id] || [];
                return users.sort(function(a, b) {
                    return b.user_rating - a.user_rating;
                });
            }
        },

        ready() {
            this.load_room_users(this.room_id);
        }
    }
</script>