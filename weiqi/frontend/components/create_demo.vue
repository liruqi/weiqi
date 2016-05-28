<template>
    <div id="qi-create-demo" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">{{$t('create_demo.header')}}</h3>
                </div>

                <div class="modal-body">
                    <div class="form-group">
                        <label for="demo-title">{{$t('game.title')}}</label>
                        <input type="text" id="demo-title" class="form-control" :placeholder="$t('create_demo.title')" v-model="title">
                    </div>

                    <div class="form-group">
                        <label for="demo-size">
                            {{$t('game.size')}}
                        </label>
                        <select id="demo-size" class="form-control" v-model="size">
                            <option :value="19" selected="selected">19x19</option>
                            <option :value="13">13x13</option>
                            <option :value="9">9x9</option>
                        </select>
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-primary" @click="create">
                        {{$t('create_demo.create')}}
                    </button>

                    <button class="btn btn-default" data-dismiss="modal">{{$t('create_demo.cancel')}}</button>
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
                title: '',
                size: 19
            }
        },

        methods: {
            create() {
                socket.send('play/create_demo', {title: this.title, size: this.size}, function(game_id) {
                    jQuery('#qi-create-demo').modal('hide');
                    this.$router.go({name: 'game', params: {game_id: game_id}});
                }.bind(this));
            }
        }
    }
</script>
