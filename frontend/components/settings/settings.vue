<template>
    <h1>{{$t('settings.header')}}</h1>

    <div class="row">
        <div class="col-xs-12 col-md-6 col-md-offset-3">
            <qi-settings-avatar></qi-settings-avatar>
            <qi-settings-user-info></qi-settings-user-info>
            <qi-settings-password></qi-settings-password>
        </div>
    </div>
</template>

<script>
    export default {
        mixins: [require('./../../mixins/title.vue')],

        components: {
            'qi-settings-avatar': require('./settings_avatar.vue'),
            'qi-settings-user-info': require('./settings_user_info.vue'),
            'qi-settings-password': require('./settings_password.vue')
        },

        computed: {
            window_title() {
                return this.$t('settings.header');
            }
        }
    }
</script>
