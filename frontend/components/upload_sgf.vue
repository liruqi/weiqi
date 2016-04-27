<template>
    <div id="qi-upload-sgf" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">{{$t('uploadSGF.header')}}</h3>
                </div>

                <div class="modal-body">
                    <div class="form-group" :class="{'has-error': !!error}">
                        <label for="sgf-input">{{$t('uploadSGF.chooseFile')}}</label>
                        <input id="sgf-input" type="file" @change="fileChosen">

                        <p v-if="!!error" class="help-block">{{error}}</p>
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-primary" @click="upload" :disabled="!sgf">
                        {{$t('uploadSGF.upload')}}
                    </button>

                    <button class="btn btn-default" data-dismiss="modal">{{$t('uploadSGF.cancel')}}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                sgf: '',
                error: ''
            }
        },

        methods: {
            fileChosen() {
                var file = jQuery('#sgf-input')[0].files[0];
                var fr = new FileReader();

                if(!file) {
                    this.sgf = '';
                    return;
                }

                fr.onload = function() {
                    this.sgf = fr.result;
                }.bind(this);

                fr.readAsText(file);
            },

            upload() {
                this.$http.post('/api/play/upload-sgf', {sgf: this.sgf}).then(function(res) {
                    jQuery('#qi-upload-sgf').modal('hide');
                    this.$router.go({name: 'game', params: {gameID: res.data}});
                }.bind(this), function() {
                    this.error = 'error';
                    this.sgf = '';
                }.bind(this))
            }
        }
    }
</script>