<template>
    <div class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            <qi-username-rank :user-id="userID" :rating="rating"></qi-username-rank>
        </a>

        <ul class="dropdown-menu">
            <li>
                <a tabindex="-1" v-link="{name: 'user', params: {userID: userID}}">
                    {{$t('user.viewProfile')}}
                </a>

                <template v-if="authUser.loggedIn && !isSelf">
                    <a tabindex="-1" v-link="{name: 'userMessage', params: {userID: userID}}">
                        {{$t('user.sendMessage')}}
                    </a>
                </template>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        props: ['userID', 'rating'],

        vuex: {
            getters: {
                authUser: function(state) { return state.auth.user; }
            }
        },

        computed: {
            isSelf() {
                return this.userID == this.authUser.userID;
            }
        }
    }
</script>