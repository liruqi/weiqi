<template>
    <div class="row" v-if="timer_started">
        <div class="col-sm-9 game-detail-left">
            <template v-if="!has_started">
                <h1 class="text-center">{{$t('game.will_start_in')}}</h1>
                <h1 class="text-center">{{seconds_to_start}}</h1>
            </template>
            <template v-else>
                <p v-if="game.is_demo && game.demo_title" class="text-center">{{game.demo_title}}</p>
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

                    <p class="text-center" v-if="game.Result">
                        {{game.Result}}
                    </p>

                    <template v-if="is_player && has_started">
                        <button class="btn btn-default btn-block" v-if="game.stage=='playing'" @click="pass()">
                            {{$t('game.pass')}}
                        </button>

                        <button class="btn btn-default btn-block" v-if="game.stage=='counting'" @click="confirmScore()">
                            {{$t('game.confirmScore')}}
                        </button>

                        <button class="btn btn-default btn-block" v-if="game.stage!='finished'" @click="resign()">
                            {{$t('game.resign')}}
                        </button>
                    </template>

                    <qi-game-navigation :game="game" :is-player="is_player" :has-control="has_control" :force_node_id.sync="force_node_id"></qi-game-navigation>
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
                    return this.game.demo_title;
                }
                return this.game.white_display + ' - ' + this.game.black_display;
            },

            game() {
                var empty = {
                    id: false,
                    timing: {
                        black: {},
                        white: {}
                    },
                    board: {
                        tree: []
                    }
                };

                return this.open_games.find(function(game) { return game.id == this.$route.params.game_id; }.bind(this)) || empty;
            },

            is_player() {
                return this.user.user_id == this.game.black_user_id || this.user.user_id == this.game.white_user_id;
            },

            has_control() {
                return this.user.user_id == this.game.demo_control_id;
            },

            black_time() {
                if(this.game.timing && this.game.timing.black) {
                    return this.formatTime(this.game.timing.black.Main);
                }
            },

            white_time() {
                if(this.game.timing && this.game.timing.white) {
                    return this.formatTime(this.game.timing.white.Main);
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
            'game.board.last_inserted_node_id': function(nodeID) {
                if(this.game.board.current_node_id != nodeID) {
                    return;
                }

                var node = this.game.board.tree[nodeID];

                // No sound for pass/resign
                if(node.Move < 0) {
                    return;
                }

                if(node.action == 'B') {
                    new Howl({src: ['/static/sounds/black.mp3', '/static/sounds/black.ogg']}).play()
                } else if(node.action == 'W') {
                    new Howl({src: ['/static/sounds/white.mp3', '/static/sounds/white.ogg']}).play()
                }
            },

            'game_has_update[$route.params.game_id]': function() {
                this.clearUpdate();
            }
        },

        ready() {
            this.open_game(this.$route.params.game_id);
            this.clearUpdate();
            this.timer = setInterval(this.updateTimer, 200);
            this.updateTimer();
        },

        destroyed() {
            clearInterval(this.timer);
        },

        events: {
            'board-click': function(coord) {
                if(this.game.is_demo && this.has_control) {
                    switch(this.demo_tool) {
                        case 'move':
                            this.$http.post('/api/games/' + this.$route.params.game_id + '/move', {move: coord});
                            break;
                    }
                } else if(!this.game.is_demo && this.is_player) {
                    if (this.game.stage == 'counting') {
                        this.$http.post('/api/games/' + this.$route.params.game_id + '/toggle-marked-dead', {coord: coord});
                    } else if (this.game.stage != 'finished') {
                        this.$http.post('/api/games/' + this.$route.params.game_id + '/move', {move: coord});
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
            clearUpdate() {
                this.clear_game_update(this.$route.params.game_id);
            },

            updateTimer() {
                if(this.game.id === false) {
                    return;
                }

                if(this.game.timing) {
                    this.seconds_to_start = Math.ceil(moment(this.game.timing.start_at).diff(moment.utc()) / 1000);

                    if (this.has_started) {
                        this.update_game_time(this.game.id);
                    }
                }

                this.timer_started = true;
            },

            pad(n) {
                return (n < 10) ? ("0" + n) : n;
            },

            formatTime(time) {
                var sec = Math.ceil(time / 1000000000);
                var min = Math.floor(sec / 60);

                sec -= min * 60;

                return this.pad(Math.round(min)) + ":" + this.pad(Math.round(sec));
            },

            pass() {
                bootbox.confirm({
                    buttons: {
                        confirm: {
                            label: this.$t('game.pass')
                        }
                    },
                    message: this.$t('game.confirmPass'),
                    callback: function (res) {
                        if (res) {
                            this.$http.post('/api/games/' + this.$route.params.game_id + '/move', {move: -1});
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
                    message: this.$t('game.confirmResign'),
                    callback: function(res) {
                        if(res) {
                            this.$http.post('/api/games/'+this.$route.params.game_id+'/move', {move: -2});
                        }
                    }.bind(this)
                });
            },

            confirmScore() {
                this.$http.post('/api/games/'+this.$route.params.game_id+'/confirm-score', {result: this.game.Result});
            }
        }
    }
</script>