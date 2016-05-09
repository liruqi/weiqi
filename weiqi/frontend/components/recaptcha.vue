<template>
    <div v-el:container></div>
</template>

<script>
    export default {
        ready() {
            grecaptcha.render(this.$els.container, {
                sitekey: '6Lekdh8TAAAAADpkqbGYDr04MQGcBJ7b42TLnR4V',
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