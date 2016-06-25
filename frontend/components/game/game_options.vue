<template>
    <div class="game-options">
        <div class="dropdown">
            <button class="btn btn-default btn-xs btn-block dropdown-toggle" type="button" data-toggle="dropdown">
                {{$t('game.options')}}
            </button>

            <ul class="dropdown-menu">
                <template v-if="game.is_demo && game.demo_owner_id == user.user_id">
                    <li>
                        <a href="#" data-toggle="modal" data-target="#edit-game-info">
                            <i class="fa fa-fw fa-info-circle"></i> {{$t('game.edit_info')}}
                        </a>
                    </li>
                </template>
                <template v-else>
                    <li>
                        <a href="#" data-toggle="modal" data-target="#game-info">
                            <i class="fa fa-fw fa-info-circle"></i> {{$t('game.info')}}
                        </a>
                    </li>
                </template>

                <template v-if="game.stage == 'finished' || !is_player">
                    <li v-if="game.demo_owner_id != user.user_id">
                        <a href="javascript:void(0)" @click="create_demo(game.id)">
                            <i class="fa fa-fw fa-desktop"></i>
                            {{$t('game.clone_demo')}}
                        </a>
                    </li>
                    <li>
                        <a :href="'/api/games/'+game.id+'/sgf'" target="_blank">
                            <i class="fa fa-fw fa-download"></i>
                            {{$t('game.download_sgf')}}
                        </a>
                    </li>
                </template>
            </ul>
        </div>

        <div id="game-info" class="modal fade">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">{{$t('game.info')}}</h3>
                    </div>

                    <div class="modal-body">
                        <table class="table table-striped table-hover">
                            <template v-if="game.is_demo">
                                <thead>
                                    <tr>
                                        <th colspan="2">{{game.title}}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <th>{{$t('game.white')}}</th>
                                        <td>{{game.white_display}}</td>
                                    </tr>
                                    <tr>
                                        <th>{{$t('game.black')}}</th>
                                        <td>{{game.black_display}}</td>
                                    </tr>
                                </tbody>
                            </template>
                            <template v-else>
                                <thead>
                                    <tr>
                                        <th colspan="2" class="text-center">
                                            <qi-username-rank :display="game.white_display" :rating="game.white_rating"></qi-username-rank>
                                            &mdash;
                                            <qi-username-rank :display="game.black_display" :rating="game.black_rating"></qi-username-rank>
                                        </th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr>
                                        <th>{{$t('game.type')}}</th>
                                        <td><qi-game-type :game="game"></qi-game-type></td>
                                    </tr>
                                    <tr>
                                        <th>{{$t('game.speed')}}</th>
                                        <td><qi-game-speed :game="game"></qi-game-speed></td>
                                    </tr>
                                    <tr>
                                        <th>{{$t('game.handicap')}}</th>
                                        <td>{{game.board.handicap}}</td>
                                    </tr>
                                    <tr>
                                        <th>{{$t('game.komi')}}</th>
                                        <td>{{game.komi.toFixed(1)}}</td>
                                    </tr>
                                    <!-- TODO: No other timings implemented
                                    <tr>
                                        <th>{{$t('game.timing')}}</th>
                                        <td>{{game.timing.system}}</td>
                                    </tr>
                                    -->
                                    <tr>
                                        <th>{{$t('game.maintime')}}</th>
                                        <td>{{format_duration(game.timing.main)}}</td>
                                    </tr>
                                    <tr>
                                        <th>{{$t('game.overtime')}}</th>
                                        <td>{{format_duration(game.timing.overtime)}}</td>
                                    </tr>
                                </tbody>
                            </template>
                        </table>
                    </div>

                    <div class="modal-footer">
                        <button class="btn btn-default" data-dismiss="modal">{{$t('general.close')}}</button>
                    </div>
                </div>
            </div>
        </div>

        <div id="edit-game-info" class="modal fade">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h3 class="modal-title">{{$t('game.info')}}</h3>
                    </div>

                    <div class="modal-body">
                        <div class="form-group">
                            <label for="game-title">{{$t('game.title')}}</label>
                            <input type="text" class="form-control" id="game-title" v-model="title">
                        </div>

                        <div class="form-group">
                            <label for="game-white">{{$t('game.white')}}</label>
                            <input type="text" class="form-control" id="game-white" v-model="white">
                        </div>

                        <div class="form-group">
                            <label for="game-black">{{$t('game.black')}}</label>
                            <input type="text" class="form-control" id="game-black" v-model="black">
                        </div>
                    </div>

                    <div class="modal-footer">
                        <button class="btn btn-primary" @click="edit_info">
                            {{$t('general.save')}}
                        </button>

                        <button class="btn btn-default" data-dismiss="modal">{{$t('general.cancel')}}</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { create_demo } from '../../vuex/actions';
    import { format_duration } from '../../format';
    import * as socket from '../../socket';

    export default {
        props: ['game', 'is_player', 'has_control'],

        data() {
            return {
                title: this.game.title,
                black: this.game.black_display,
                white: this.game.white_display
            }
        },

        ready() {
            jQuery('#edit-game-info').appendTo('body');
            jQuery('#game-info').appendTo('body');
        },

        destroyed() {
            jQuery('body > #edit-game-info').remove();
            jQuery('body > #game-info').remove();
        },

        vuex: {
            getters: {
                user: function(state) { return state.auth.user }
            },
            actions: {
                create_demo
            }
        },

        methods: {
            format_duration,

            edit_info() {
                var data = {
                    game_id: this.game.id,
                    title: this.title,
                    black_display: this.black,
                    white_display: this.white
                };

                socket.send('games/edit_info', data, function() {
                    jQuery('#edit-game-info').modal('hide');
                });
            }
        }
    }
</script>