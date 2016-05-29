<template>
     <div id="qi-disconnected" class="modal fade" data-keyboard="false" data-backdrop="static">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">{{$t('disconnected.header')}}</h3>
                </div>
                <div class="modal-body">
                    <p>{{{$t('disconnected.body')}}}</p>
                    <br>
                    <p><i class="fa fa-spinner fa-spin fa-fw"></i> {{$t('disconnected.trying_connect')}}</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        ready() {
            jQuery('#qi-disconnected').on('shown.bs.modal', function() {
                setInterval(function() {
                    this.$http.get('/api/ping').then(function(res) {
                        if (res.data == "pong") {
                            window.location.reload(true);
                        }
                    });
                }.bind(this), 5000);
            }.bind(this));
        }
    }
</script>