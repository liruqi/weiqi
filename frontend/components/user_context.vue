<template>
    <div class="dropdown">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            <qi-username-rank :display="display" :rating="rating"></qi-username-rank>
        </a>

        <ul class="dropdown-menu">
            <li>
                <a tabindex="-1" v-link="{name: 'user', params: {user_id: user_id}}">
                    {{$t('user.view_profile')}}
                </a>

                <template v-if="auth_user.logged_in && !is_self">
                    <a tabindex="-1" v-link="{name: 'user_message', params: {user_id: user_id}}">
                        {{$t('user.send_message')}}
                    </a>
                </template>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        props: ['user_id', 'display', 'rating'],

        vuex: {
            getters: {
                auth_user: function(state) { return state.auth.user; }
            }
        },

        computed: {
            is_self() {
                return this.user_id == this.auth_user.user_id;
            }
        }
    }
</script>