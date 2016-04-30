<template>
    <i class="fa fa-signal" :class="{
        'text-danger': connection==0,
        'text-warning': connection==1,
        'text-success': connection==2}" :title="pong+'ms'"></i>
</template>

<script>
    export default {
        vuex: {
            getters: {
                pong(state) { return state.pong }
            }
        },

        data() {
            return {
                connection: 2,
            }
        },

        computed: {
            status() {
                if(!this.pong) {
                    return 0;
                }

                if(this.pong < 100) {
                    return 2;
                }

                if(this.pong < 1000) {
                    return 1;
                }

                return 0;
            }
        }
    }
</script>