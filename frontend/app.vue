<template>
    <template v-if="loaded">
        <div class="main-wrapper" :class="{'sidebar-out': sidebar.open}">
            <qi-header></qi-header>

            <div class="main-content">
                <router-view></router-view>
            </div>

            <qi-sidebar></qi-sidebar>
        </div>

        <qi-sign-in></qi-sign-in>
        <qi-play-dialog></qi-play-dialog>
        <qi-create-demo></qi-create-demo>
        <qi-upload-sgf></qi-upload-sgf>
        <qi-challenge></qi-challenge>
        <qi-disconnected></qi-disconnected>
    </template>

    <template v-else>
        <slot>
            <qi-page-load-spinner></qi-page-load-spinner>
        </slot>
    </template>
</template>

<script>
    import store from './vuex/store';
    import { update_route } from './vuex/actions';
    import { request_notify_permission } from './notify';

    export default {
        store: store,
        mixins: [require('./mixins/update_handler.vue'), require('./mixins/notifications.vue')],

        vuex: {
            getters: {
                loaded: function(state) { return state.loaded; },
                sidebar: function(state) { return state.sidebar; }
            },
            actions: {
                update_route
            }
        },

        watch: {
            '$route.path': function() {
                this.update_route(this.$route);
                this.scroll_to_anchor();
            },

            'loaded': function() {
                request_notify_permission();
                this.scroll_to_anchor();
            }
        },

        ready() {
            this.update_route(this.$route);
        },

        methods: {
            scroll_to_anchor() {
                if(window.location.hash != '') {
                    this.$nextTick(function() {
                        var el = jQuery(window.location.hash);
                        if (el.length > 0) {
                            jQuery('.main-wrapper').scrollTop(el.offset().top - jQuery('.main-header .navbar').height() - 10);
                        }
                    });
                }
            }
        }
    }
</script>
