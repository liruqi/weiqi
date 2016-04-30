<template>
    <div id="qi-create-demo" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">{{$t('createDemo.header')}}</h3>
                </div>

                <div class="modal-body">
                    <div class="form-group">
                        <input type="text" class="form-control" :placeholder="$t('createDemo.title')" v-model="title">
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
                        {{$t('createDemo.create')}}
                    </button>

                    <button class="btn btn-default" data-dismiss="modal">{{$t('createDemo.cancel')}}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                title: '',
                size: 19
            }
        },

        methods: {
            create() {
                this.$http.post('/api/play/create-demo', {title: this.title, size: this.size}).then(function(res) {
                    jQuery('#qi-create-demo').modal('hide');
                    this.$router.go({name: 'game', params: {game_id: res.data}});
                }.bind(this));
            }
        }
    }
</script>
