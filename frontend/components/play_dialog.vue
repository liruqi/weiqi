<template>
    <div id="qi-play-dialog" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">
                        {{$t('play.header')}}
                        <small>{{$t('play.subheader')}}</small>
                    </h3>
                </div>

                <div class="modal-body">
                    <div class="preset" :class="{active: preset=='fast'}" @click="presetFast">
                        <p class="preset-name">{{$t('play.fast.header')}}</p>
                        <p class="preset-description">
                            {{$t('play.fast.l1')}}<br>
                            {{$t('play.fast.l2')}}
                        </p>
                    </div>
                    <div class="preset" :class="{active: preset=='medium'}" @click="presetMedium">
                        <p class="preset-name">{{$t('play.medium.header')}}</p>
                        <p class="preset-description">
                            {{$t('play.medium.l1')}}<br>
                            {{$t('play.medium.l2')}}
                        </p>
                    </div>
                    <div class="preset" :class="{active: preset=='slow'}" @click="presetSlow">
                        <p class="preset-name">{{$t('play.slow.header')}}</p>
                        <p class="preset-description">
                            {{$t('play.slow.l1')}}<br>
                            {{$t('play.slow.l2')}}
                        </p>
                    </div>
                    <div class="preset" :class="{active: preset=='correspondence'}" @click="presetCorrespondence">
                        <p class="preset-name">{{$t('play.corr.header')}}</p>
                        <p class="preset-description">
                            {{$t('play.corr.l1')}}<br>
                            {{$t('play.corr.l2')}}
                        </p>
                    </div>

                    <div class="form-horizontal">
                        <div class="form-group">
                            <label class="col-sm-4 control-label">{{$t('play.options.max_hc')}}</label>
                            <div class="col-sm-8">
                                <select class="form-control" v-model="max_hc">
                                    <option :value="0">{{$t('play.options.no_hc')}}</option>
                                    <option :value="1">1</option>
                                    <option :value="2">2</option>
                                    <option :value="3">3</option>
                                    <option :value="4">4</option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-primary" @click="play">
                        {{$t('play.play')}}
                    </button>

                    <button class="btn btn-default" data-dismiss="modal">{{$t('play.cancel')}}</button>
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
                preset: 'medium',
                max_hc: 4
            }
        },

        methods: {
            presetFast() {
                this.preset = 'fast';
            },
            presetMedium() {
                this.preset = 'medium';
            },
            presetSlow() {
                this.preset = 'slow';
            },
            presetCorrespondence() {
                this.preset = 'correspondence';
            },

            play() {
                socket.send('play/automatch', {preset: this.preset, max_hc: this.max_hc}, function() {
                    jQuery('#qi-play-dialog').modal('hide');
                });
            }
        }
    }
</script>