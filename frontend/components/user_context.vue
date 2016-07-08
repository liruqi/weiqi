<template>
    <div class="dropdown user-context">
        <a href="#" class="dropdown-toggle" data-toggle="dropdown">
            <qi-username-rank :display="display" :rating="rating"></qi-username-rank>
        </a>

        <ul class="dropdown-menu" :class="{'dropdown-menu-right': align=='right'}">
            <li>
                <a tabindex="-1" v-link="{name: 'user', params: {user_id: user_id}}">
                    <i class="fa fa-user fa-fw"></i> {{$t('user.view_profile')}}
                </a>

                <template v-if="auth_user.logged_in && !is_self">
                    <a tabindex="-1" v-link="{name: 'user_message', params: {user_id: user_id}}">
                        <i class="fa fa-envelope fa-fw"></i> {{$t('user.send_message')}}
                    </a>
                    <a tabindex="-1" href="javascript:void(0)" @click="challenge_user">
                        <i class="fa fa-trophy fa-fw"></i> {{$t('user.challenge')}}
                    </a>
                </template>
            </li>
        </ul>
    </div>
</template>

<script>
    export default {
        props: ['user_id', 'display', 'rating', 'align'],

        vuex: {
            getters: {
                auth_user: function(state) { return state.auth.user; }
            }
        },

        computed: {
            is_self() {
                return this.user_id == this.auth_user.user_id;
            }
        },

        methods: {
            challenge_user() {
                jQuery('#challenge-user').trigger('qi:set_user', this.user_id);
                jQuery("#qi-challenge").modal("show");
            }
        }
    }
</script>