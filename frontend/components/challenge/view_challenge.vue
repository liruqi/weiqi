<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            {{$t('challenge.view.heading')}}

            <span v-if="challenge">
                &mdash;
                <qi-username-rank :display="opponent_display" :rating="opponent_rating"></qi-username-rank>
            </span>
        </div>

        <div v-if="!challenge" class="panel-body">
            <p class="text-center lead">
                {{$t('challenge.view.not_found')}}
            </p>
        </div>
        <table v-else class="table table-hover">
            <tr>
                <td style="width:50%;">
                    <p class="text-center">
                        <img :src="'/api/users/' + white.id + '/avatar'" class="avatar">
                    </p>
                    <p class="text-center">
                        <i class="fa fa-circle-thin"></i>
                        &nbsp;&nbsp;
                        <qi-user-context :user_id="white.id" :display="white.display" :rating="white.rating"></qi-user-context>
                    </p>
                </td>
                <td style="width:50%;">
                    <p class="text-center">
                        <img :src="'/api/users/' + black.id + '/avatar'" class="avatar">
                    </p>
                    <p class="text-center">
                        <i class="fa fa-circle"></i>
                        &nbsp;&nbsp;
                        <qi-user-context :user_id="black.id" :display="black.display" :rating="black.rating"></qi-user-context>
                    </p>
                </td>
            </tr>
            <tr>
                <th>{{$t('game.type')}}</th>
                <td>
                    <qi-game-type :game="challenge"></qi-game-type>
                </td>
            </tr>
            <tr>
                <th>{{$t('game.board_size')}}</th>
                <td>{{challenge.board_size}}x{{challenge.board_size}}</td>
            </tr>
            <tr>
                <th>{{$t('game.handicap')}}</th>
                <td>{{challenge.handicap}}</td>
            </tr>
            <tr>
                <th>{{$t('game.komi')}}</th>
                <td>{{challenge.komi}}</td>
            </tr>
            <tr>
                <th>{{$t('game.speed')}}</th>
                <td><qi-game-speed :game="challenge"></qi-game-speed></td>
            </tr>
            <!-- TODO: No other timings implemented
            <tr>
                <th>{{$t('game.timing')}}</th>
                <td>{{challenge.timing_system}}</td>
            </tr>
            -->
            <tr>
                <th>{{$t('game.maintime')}}</th>
                <td>{{format_duration(challenge.maintime)}}</td>
            </tr>
            <tr>
                <th>{{$t('game.overtime')}}</th>
                <td>{{format_duration(challenge.overtime)}}</td>
            </tr>
            <tr>
                <th>{{$t('challenge.view.expires_in')}}</th>
                <td>{{expires_in}}</td>
            </tr>
            <tr>
                <template v-if="is_owner">
                    <td colspan="2">
                        <button type="button" class="btn btn-default btn-block" @click="cancel">
                            {{$t('challenge.view.cancel')}}
                        </button>
                    </td>
                </template>
                <template v-else>
                    <td>
                        <button type="button" class="btn btn-success btn-block" @click="accept">
                            {{$t('challenge.view.accept')}}
                        </button>
                    </td>
                    <td>
                        <button type="button" class="btn btn-default btn-block" @click="decline">
                            {{$t('challenge.view.decline')}}
                        </button>
                    </td>
                </template>
            </tr>
        </table>
    </div>
</template>

<script>
    import moment from 'moment';
    import * as socket from '../../socket';
    import { format_duration } from '../../format';

    export default {
        mixins: [require('./../../mixins/title.vue')],

        data() {
            return {
                expires_in: '',
                timer: null
            }
        },

        vuex: {
            getters: {
                challenges: function(state) { return state.challenges; },
                user: function(state) { return state.auth.user; }
            }
        },

        route: {
            canReuse: false
        },

        ready() {
            this.timer = setInterval(this.update_timer, 200);
            this.update_timer();
        },

        destroyed() {
            clearInterval(this.timer);
        },

        computed: {
            window_title() {
                if(!this.challenge) {
                    return '';
                }
                return this.opponent_display;
            },

            challenge() {
                return this.challenges.find(function(ch) {
                    return ch.id == this.$route.params.challenge_id;
                }.bind(this));
            },

            is_owner() {
                return (this.user.user_id == this.challenge.owner_id);
            },

            opponent_display() {
                if(this.is_owner) {
                    return this.challenge.challengee_display;
                }
                return this.challenge.owner_display;
            },

            opponent_rating() {
                if(this.is_owner) {
                    return this.challenge.challengee_rating;
                }
                return this.challenge.owner_rating;
            },

            black_white() {
                var black = {
                    id: this.challenge.owner_id,
                    display: this.challenge.owner_display,
                    rating: this.challenge.owner_rating
                };

                var white = {
                    id: this.challenge.challengee_id,
                    display: this.challenge.challengee_display,
                    rating: this.challenge.challengee_rating
                };

                if(!this.challenge.owner_is_black) {
                    var tmp = black;
                    black = white;
                    white = tmp;
                }

                return [black, white];
            },

            black() {
                return this.black_white[0];
            },

            white() {
                return this.black_white[1];
            }
        },

        methods: {
            format_duration: format_duration,

            update_timer() {
                if(!this.challenge) {
                    return;
                }

                var secs = Math.ceil(moment.utc(this.challenge.expire_at).diff(moment.utc()) / 1000);
                this.expires_in = format_duration(secs);
            },

            cancel() {
                socket.send('play/cancel_challenge', {challenge_id: this.challenge.id}, function() {
                    this.$router.go({name: 'root'});
                }.bind(this));
            },

            accept() {
                socket.send('play/accept_challenge', {challenge_id: this.challenge.id}, function() {
                }.bind(this));
            },

            decline() {
                socket.send('play/decline_challenge', {challenge_id: this.challenge.id}, function() {
                    this.$router.go({name: 'root'});
                }.bind(this));
            }
        }
    }
</script>