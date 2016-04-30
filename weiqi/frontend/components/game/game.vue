<template>
    <div class="row" v-if="timerStarted">
        <div class="col-sm-9 game-detail-left">
            <template v-if="!hasStarted">
                <h1 class="text-center">{{$t('game.willStartIn')}}</h1>
                <h1 class="text-center">{{secondsToStart}}</h1>
            </template>
            <template v-else>
                <p v-if="game.Demo && game.DemoTitle" class="text-center">{{game.DemoTitle}}</p>
                <qi-board v-if="game.Board" :board="game.Board" :force_node_id="force_node_id" :coordinates="coordinates"></qi-board>
            </template>
        </div>

        <div class="col-sm-3 game-detail-right">
            <div class="panel panel-default flex-fixed game-detail-players">
                <div class="panel-body">
                    <div class="row">
                        <div class="col-xs-6">
                            <qi-game-player :demo="game.Demo" :stage="game.stage" :color="'white'"
                                            :demo-player="game.DemoWhite" :player="game.MatchWhite"
                                            :rating="game.MatchWhiteRating" :points="0" :time="whiteTime"></qi-game-player>
                        </div>
                        <div class="col-xs-6">
                            <qi-game-player :demo="game.Demo" :stage="game.stage" :color="'black'"
                                            :demo-player="game.DemoBlack" :player="game.MatchBlack"
                                            :rating="game.MatchBlackRating" :points="0" :time="blackTime"></qi-game-player>
                        </div>
                    </div>

                    <p class="text-center" v-if="game.Result">
                        {{game.Result}}
                    </p>

                    <template v-if="isPlayer && hasStarted">
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

                    <qi-game-navigation :game="game" :is-player="isPlayer" :has-control="hasControl" :force_node_id.sync="force_node_id"></qi-game-navigation>
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
                secondsToStart: 0,
                timerStarted: false,
                demoTool: 'move'
            }
        },

        computed: {
            windowTitle() {
                if(this.game.Demo) {
                    return this.game.DemoTitle;
                }
                return this.game.MatchWhite + ' - ' + this.game.MatchBlack;
            },

            game() {
                var empty = {
                    ID: false,
                    Timing: {
                        Black: {},
                        White: {}
                    },
                    Board: {
                        Tree: []
                    }
                };

                return this.open_games.find(function(game) { return game.id == this.$route.params.game_id; }.bind(this)) || empty;
            },

            isPlayer() {
                return this.user.user_id == this.game.MatchBlack || this.user.user_id == this.game.MatchWhite;
            },

            hasControl() {
                return this.user.user_id == this.game.DemoControl;
            },

            blackTime() {
                if(this.game.Timing && this.game.Timing.Black) {
                    return this.formatTime(this.game.Timing.Black.Main);
                }
            },

            whiteTime() {
                if(this.game.Timing && this.game.Timing.White) {
                    return this.formatTime(this.game.Timing.White.Main);
                }
            },

            hasStarted() {
                return this.secondsToStart <= 0;
            },

            room_logs_show_only() {
                if(this.isPlayer && this.game.stage != 'finished') {
                    return [this.game.MatchBlack, this.game.MatchWhite];
                }
                return [];
            },

            coordinates() {
                return !this.isPlayer || this.game.stage == 'finished';
            }
        },

        watch: {
            'game.Board.LastInsertedNodeID': function(nodeID) {
                if(this.game.Board.CurrentNodeID != nodeID) {
                    return;
                }

                var node = this.game.Board.Tree[nodeID];

                // No sound for pass/resign
                if(node.Move < 0) {
                    return;
                }

                if(node.Action == 'B') {
                    new Howl({src: ['/assets/sounds/black.mp3', '/assets/sounds/black.ogg']}).play()
                } else if(node.Action == 'W') {
                    new Howl({src: ['/assets/sounds/white.mp3', '/assets/sounds/white.ogg']}).play()
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
                if(this.game.Demo && this.hasControl) {
                    switch(this.demoTool) {
                        case 'move':
                            this.$http.post('/api/games/' + this.$route.params.game_id + '/move', {move: coord});
                            break;
                    }
                } else if(!this.game.Demo && this.isPlayer) {
                    if (this.game.stage == 'counting') {
                        this.$http.post('/api/games/' + this.$route.params.game_id + '/toggle-marked-dead', {coord: coord});
                    } else if (this.game.stage != 'finished') {
                        this.$http.post('/api/games/' + this.$route.params.game_id + '/move', {move: coord});
                    }
                }
            },

            'board-scroll': function(scroll) {
                if(this.game.Demo || (this.isPlayer && this.game.stage != 'finished')) {
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

                if(this.game.Timing) {
                    this.secondsToStart = Math.ceil(moment(this.game.Timing.StartAt).diff(moment.utc()) / 1000);

                    if (this.hasStarted) {
                        this.update_game_time(this.game.id);
                    }
                }

                this.timerStarted = true;
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