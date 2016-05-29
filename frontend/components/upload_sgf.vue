<template>
    <div id="qi-upload-sgf" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">{{$t('upload_sgf.header')}}</h3>
                </div>

                <div class="modal-body">
                    <div class="form-group" :class="{'has-error': !!error}">
                        <label for="sgf-input">{{$t('upload_sgf.choose_file')}}</label>
                        <input id="sgf-input" type="file" @change="file_chosen">

                        <p v-if="!!error" class="help-block">{{error}}</p>
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-primary" @click="upload" :disabled="!sgf">
                        {{$t('upload_sgf.upload')}}
                    </button>

                    <button class="btn btn-default" data-dismiss="modal">{{$t('upload_sgf.cancel')}}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import * as socket from '../socket';

    export default {
        data() {
            return {
                sgf: '',
                error: ''
            }
        },

        methods: {
            file_chosen() {
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
                socket.send('play/upload_sgf', {sgf: this.sgf}, function(game_id) {
                    jQuery('#qi-upload-sgf').modal('hide');
                    this.$router.go({name: 'game', params: {game_id: game_id}});
                }.bind(this)/*, function() {
                    this.error = 'error';
                    this.sgf = '';
                }.bind(this)*/);
            }
        }
    }
</script>