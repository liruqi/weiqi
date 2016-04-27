<template>
    <h1>{{msg}}</h1>
</template>

<script>
    export default {
        mixins: [require('./../mixins/title.vue')],

        data () {
            return {
                msg: 'Home'
            }
        }
    }
</script>
