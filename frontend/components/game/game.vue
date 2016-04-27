<template>
    <div class="row" v-if="timerStarted">
        <div class="col-sm-9 game-detail-left">
            <template v-if="!hasStarted">
                <h1 class="text-center">{{$t('game.willStartIn')}}</h1>
                <h1 class="text-center">{{secondsToStart}}</h1>
            </template>
            <template v-else>
                <p v-if="game.Demo && game.DemoTitle" class="text-center">{{game.DemoTitle}}</p>
                <qi-board v-if="game.Board" :board="game.Board" :force-node-id="forceNodeID" :coordinates="coordinates"></qi-board>
            </template>
        </div>

        <div class="col-sm-3 game-detail-right">
            <div class="panel panel-default flex-fixed game-detail-players">
                <div class="panel-body">
                    <div class="row">
                        <div class="col-xs-6">
                            <qi-game-player :demo="game.Demo" :stage="game.Stage" :color="'white'"
                                            :demo-player="game.DemoWhite" :player="game.MatchWhite"
                                            :rating="game.MatchWhiteRating" :points="0" :time="whiteTime"></qi-game-player>
                        </div>
                        <div class="col-xs-6">
                            <qi-game-player :demo="game.Demo" :stage="game.Stage" :color="'black'"
                                            :demo-player="game.DemoBlack" :player="game.MatchBlack"
                                            :rating="game.MatchBlackRating" :points="0" :time="blackTime"></qi-game-player>
                        </div>
                    </div>

                    <p class="text-center" v-if="game.Result">
                        {{game.Result}}
                    </p>

                    <template v-if="isPlayer && hasStarted">
                        <button class="btn btn-default btn-block" v-if="game.Stage=='playing'" @click="pass()">
                            {{$t('game.pass')}}
                        </button>

                        <button class="btn btn-default btn-block" v-if="game.Stage=='counting'" @click="confirmScore()">
                            {{$t('game.confirmScore')}}
                        </button>

                        <button class="btn btn-default btn-block" v-if="game.Stage!='finished'" @click="resign()">
                            {{$t('game.resign')}}
                        </button>
                    </template>

                    <qi-game-navigation :game="game" :is-player="isPlayer" :has-control="hasControl" :force-node-id.sync="forceNodeID"></qi-game-navigation>
                </div>
            </div>

            <qi-room-users :room-id="game.RoomID"></qi-room-users>
            <qi-room-logs :room-id="game.RoomID" :show-only-user-ids="roomLogsShowOnly"></qi-room-logs>
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
    import { openGame, updateGameTime, clearGameUpdate } from './../../vuex/actions';

    export default {
        mixins: [require('./../../mixins/title.vue')],

        components: {
            'qi-game-player': require('./game_player.vue'),
            'qi-game-navigation': require('./game_navigation.vue')
        },

        vuex: {
            getters: {
                openGames: function(state) { return state.openGames },
                user: function(state) { return state.auth.user },
                gameHasUpdate: function(state) { return state.gameHasUpdate; }
            },
            actions: {
                openGame,
                updateGameTime,
                clearGameUpdate
            }
        },

        route: {
            canReuse: false
        },

        data() {
            return {
                forceNodeID: false,
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

                return this.openGames.find(function(game) { return game.ID == this.$route.params.gameID; }.bind(this)) || empty;
            },

            isPlayer() {
                return this.user.userID == this.game.MatchBlack || this.user.userID == this.game.MatchWhite;
            },

            hasControl() {
                return this.user.userID == this.game.DemoControl;
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

            roomLogsShowOnly() {
                if(this.isPlayer && this.game.Stage != 'finished') {
                    return [this.game.MatchBlack, this.game.MatchWhite];
                }
                return [];
            },

            coordinates() {
                return !this.isPlayer || this.game.Stage == 'finished';
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

            'gameHasUpdate[$route.params.gameID]': function() {
                this.clearUpdate();
            }
        },

        ready() {
            this.openGame(this.$route.params.gameID);
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
                            this.$http.post('/api/games/' + this.$route.params.gameID + '/move', {move: coord});
                            break;
                    }
                } else if(!this.game.Demo && this.isPlayer) {
                    if (this.game.Stage == 'counting') {
                        this.$http.post('/api/games/' + this.$route.params.gameID + '/toggle-marked-dead', {coord: coord});
                    } else if (this.game.Stage != 'finished') {
                        this.$http.post('/api/games/' + this.$route.params.gameID + '/move', {move: coord});
                    }
                }
            },

            'board-scroll': function(scroll) {
                if(this.game.Demo || (this.isPlayer && this.game.Stage != 'finished')) {
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
                this.clearGameUpdate(this.$route.params.gameID);
            },

            updateTimer() {
                if(this.game.ID === false) {
                    return;
                }

                if(this.game.Timing) {
                    this.secondsToStart = Math.ceil(moment(this.game.Timing.StartAt).diff(moment.utc()) / 1000);

                    if (this.hasStarted) {
                        this.updateGameTime(this.game.ID);
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
                            this.$http.post('/api/games/' + this.$route.params.gameID + '/move', {move: -1});
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
                            this.$http.post('/api/games/'+this.$route.params.gameID+'/move', {move: -2});
                        }
                    }.bind(this)
                });
            },

            confirmScore() {
                this.$http.post('/api/games/'+this.$route.params.gameID+'/confirm-score', {result: this.game.Result});
            }
        }
    }
</script>