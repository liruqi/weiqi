<template>
    <div v-el:container></div>
</template>

<script>
    export default {
        ready() {
            grecaptcha.render(this.$els.container, {
                sitekey: '6LcuURwTAAAAAKCKagvscwkp5p6mL_YesB3Kao7G',
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