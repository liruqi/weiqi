<template>
    <i class="fa fa-fw fa-signal" :class="{
        'text-danger': connection==0,
        'text-warning': connection==1,
        'text-success': connection==2}" :title="ms+'ms'"></i>
</template>

<script>
    import * as socket from '../socket';

    export default {
        data() {
            return {
                connection: 2,
                timer: null,
                ms: 0
            }
        },

        ready() {
            this.timer = setInterval(this.check, 60*1000);
            setTimeout(this.check, 3000);
        },

        destroyed() {
            clearInterval(this.timer);
        },

        methods: {
            check() {
                var start = (new Date()).getTime();

                socket.send('connection/ping', {}, function(data) {
                    this.ms = (new Date()).getTime() - start;

                    if(data != "pong") {
                        this.connection = 0;
                    } else if(this.ms < 300) {
                        this.connection = 2;
                    } else if(this.ms < 1000) {
                        this.connection = 1;
                    } else {
                        this.connection = 0;
                    }
                }.bind(this));
            }
        }
    }
</script>
