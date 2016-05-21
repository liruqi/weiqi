<template>
    <div v-el:container></div>
</template>

<script>
    export default {
        ready() {
            grecaptcha.render(this.$els.container, {
                sitekey: SETTINGS.RECAPTCHA_PUBLIC_KEY,
                callback: this.recaptchaCallback
            });
        },

        methods: {
            recaptchaCallback() {
                this.$dispatch('recaptcha-response', jQuery('#g-recaptcha-response').val());
            }
        }
    }
</script>