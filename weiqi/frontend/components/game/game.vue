<template>
    <div class="row" v-if="timer_started">
        <div class="col-sm-9 game-detail-left">
            <template v-if="!has_started">
                <h1 class="text-center">{{$t('game.will_start_in')}}</h1>
                <h1 class="text-center">{{seconds_to_start}}</h1>
            </template>
            <template v-else>
                <p v-if="game.is_demo" class="text-center">
                    <span v-if="game.title">{{game.title}}</span>
                    <select v-if="has_control" v-model="demo_tool" class="pull-right">
                        <option value="move">{{$t('demo.tool.move')}}</option>
                        <option value="edit">{{$t('demo.tool.edit')}}</option>
                        <option value="triangle">{{$t('demo.tool.triangle')}}</option>
                        <option value="square">{{$t('demo.tool.square')}}</option>
                        <option value="circle">{{$t('demo.tool.circle')}}</option>
                        <option value="label">{{$t('demo.tool.label')}}</option>
                        <option value="number">{{$t('demo.tool.number')}}</option>
                    </select>
                    <div class="clearfix"></div>
                </p>
                <qi-board v-if="game.board" :board="game.board" :force_node_id="force_node_id" :coordinates="coordinates"></qi-board>
            </template>
        </div>

        <div class="col-sm-3 game-detail-right">
            <div class="panel panel-default flex-fixed game-detail-players">
                <div class="panel-body">
                    <div class="row">
                        <div class="col-xs-6">
                            <qi-game-player :demo="game.is_demo" :stage="game.stage" :color="'white'"
                                            :display="game.white_display" :user_id="game.white_user_id"
                                            :rating="game.white_rating" :points="0" :time="white_time"></qi-game-player>
                        </div>
                        <div class="col-xs-6">
                            <qi-game-player :demo="game.is_demo" :stage="game.stage" :color="'black'"
                                            :display="game.black_display" :user_id="game.black_user_id"
                                            :rating="game.black_rating" :points="0" :time="black_time"></qi-game-player>
                        </div>
                    </div>

                    <p class="text-center" v-if="game.result">
                        {{game.result}}
                    </p>

                    <template v-if="is_player && has_started">
                        <button class="btn btn-default btn-block" v-if="game.stage=='playing'" @click="pass()">
                            {{$t('game.pass')}}
                        </button>

                        <button class="btn btn-default btn-block" v-if="game.stage=='counting'" @click="confirm_score()">
                            {{$t('game.confirm_score')}}
                        </button>

                        <button class="btn btn-default btn-block" v-if="game.stage!='finished'" @click="resign()">
                            {{$t('game.resign')}}
                        </button>
                    </template>

                    <qi-game-navigation :game="game" :is_player="is_player" :has_control="has_control" :force_node_id.sync="force_node_id"></qi-game-navigation>
                </div>
            </div>

            <qi-room-users :room_id="game.room_id"></qi-room-users>
            <qi-room-logs :room_id="game.room_id" :show_only_user_ids="room_logs_show_only"></qi-room-logs>
        </div>
    </div>
    <div v-else>
        <qi-page-load-spinner></qi-page-load-spinner>
    </div>
</template>

<script>
    import bootbox from 'bootbox';
    import { Howl } from 'howler';
    import moment from 'moment';
    import { open_game, update_game_time, clear_game_update } from './../../vuex/actions';
    import * as socket from '../../socket';
    import { format_duration } from '../../format';

    export default {
        mixins: [require('./../../mixins/title.vue')],

        components: {
            'qi-game-player': require('./game_player.vue'),
            'qi-game-navigation': require('./game_navigation.vue')
        },

        vuex: {
            getters: {
                open_games: function(state) { return state.open_games },
                user: function(state) { return state.auth.user },
                game_has_update: function(state) { return state.game_has_update; }
            },
            actions: {
                open_game,
                update_game_time,
                clear_game_update
            }
        },

        route: {
            canReuse: false
        },

        data() {
            return {
                force_node_id: false,
                seconds_to_start: 0,
                timer_started: false,
                demo_tool: 'move'
            }
        },

        computed: {
            window_title() {
                if(this.game.is_demo) {
                    return this.game.title;
                }
                return this.game.white_display + ' - ' + this.game.black_display;
            },

            game_id() {
                return this.$route.params.game_id;
            },

            game() {
                var empty = {
                    id: false,
                    timing: {
                        black_main: 0,
                        black_overtime: 0,
                        white_main: 0,
                        white_overtime: 0
                    },
                    board: {
                        tree: []
                    }
                };

                return this.open_games.find(function(game) { return game.id == this.game_id; }.bind(this)) || empty;
            },

            is_player() {
                return this.user.user_id == this.game.black_user_id || this.user.user_id == this.game.white_user_id;
            },

            has_control() {
                return this.user.user_id == this.game.demo_control_id;
            },

            black_time() {
                if(this.game.timing) {
                    return this.format_duration(this.game.timing.black_main);
                }
            },

            white_time() {
                if(this.game.timing) {
                    return this.format_duration(this.game.timing.white_main);
                }
            },

            has_started() {
                return this.seconds_to_start <= 0;
            },

            room_logs_show_only() {
                if(this.is_player && this.game.stage != 'finished') {
                    return [this.game.black_user_id, this.game.white_user_id];
                }
                return [];
            },

            coordinates() {
                return !this.is_player || this.game.stage == 'finished';
            }
        },

        watch: {
            'game.board.last_inserted_node_id': function(node_id) {
                if(this.game.board.current_node_id != node_id) {
                    return;
                }

                var node = this.game.board.tree[node_id];

                // No sound for pass/resign
                if(node.move < 0) {
                    return;
                }

                if(node.action == 'B') {
                    new Howl({src: ['/static/sounds/black.mp3', '/static/sounds/black.ogg']}).play()
                } else if(node.action == 'W') {
                    new Howl({src: ['/static/sounds/white.mp3', '/static/sounds/white.ogg']}).play()
                }
            },

            'game_has_update[game_id]': function() {
                this.clear_update();
            }
        },

        ready() {
            this.open_game(this.game_id);
            this.clear_update();
            this.timer = setInterval(this.update_timer, 200);
            this.update_timer();
        },

        destroyed() {
            clearInterval(this.timer);
        },

        events: {
            'board-click': function(coord, event) {
                if(this.game.is_demo && this.has_control) {
                    switch(this.demo_tool) {
                        case 'move':
                            socket.send('games/move', {game_id: this.game_id, move: coord});
                            break;
                        case 'edit':
                            if(event.shiftKey) {
                                socket.send('games/demo_tool_edit', {game_id: this.game_id, coord: coord, color: 'o'});
                            } else {
                                socket.send('games/demo_tool_edit', {game_id: this.game_id, coord: coord, color: 'x'});
                            }
                            break;
                        case 'triangle':
                            socket.send('games/demo_tool_triangle', {game_id: this.game_id, coord: coord});
                            break;
                        case 'square':
                            socket.send('games/demo_tool_square', {game_id: this.game_id, coord: coord});
                            break;
                        case 'circle':
                            socket.send('games/demo_tool_circle', {game_id: this.game_id, coord: coord});
                            break;
                        case 'label':
                            socket.send('games/demo_tool_label', {game_id: this.game_id, coord: coord});
                            break;
                        case 'number':
                            socket.send('games/demo_tool_number', {game_id: this.game_id, coord: coord});
                            break;
                    }
                } else if(!this.game.is_demo && this.is_player) {
                    if (this.game.stage == 'counting') {
                        socket.send('games/toggle_marked_dead', {'game_id': this.game_id, 'coord': coord});
                    } else if (this.game.stage != 'finished') {
                        socket.send('games/move', {'game_id': this.game_id, 'move': coord});
                    }
                }
            },

            'board-scroll': function(scroll) {
                if(this.game.is_demo || (this.is_player && this.game.stage != 'finished')) {
                    return;
                }

                if(scroll < 0) {
                    this.$broadcast("game-navigate", -1);
                } else {
                    this.$broadcast("game-navigate", +1);
                }
            }
        },

        methods: {
            format_duration: format_duration,

            clear_update() {
                this.clear_game_update(this.game_id);
            },

            update_timer() {
                if(this.game.id === false) {
                    return;
                }

                if(this.game.timing) {
                    this.seconds_to_start = Math.ceil(moment.utc(this.game.timing.start_at).diff(moment.utc()) / 1000);

                    if(this.has_started) {
                        this.update_game_time(this.game.id);
                    }
                }

                this.timer_started = true;
            },

            pass() {
                bootbox.confirm({
                    buttons: {
                        confirm: {
                            label: this.$t('game.pass')
                        }
                    },
                    message: this.$t('game.confirm_pass'),
                    callback: function (res) {
                        if (res) {
                            socket.send('games/move', {'game_id': this.game_id, 'move': -1});
                        }
                    }.bind(this)
                });
            },

            resign() {
                bootbox.confirm({
                    buttons: {
                        confirm: {
                            label: this.$t('game.resign'),
                            className: 'btn-danger'
                        }
                    },
                    message: this.$t('game.confirm_resign'),
                    callback: function(res) {
                        if(res) {
                            socket.send('games/move', {'game_id': this.game_id, 'move': -2});
                        }
                    }.bind(this)
                });
            },

            confirm_score() {
                socket.send('games/confirm_score', {'game_id': this.game_id, 'result': this.game.result});
            }
        }
    }
</script>