<template>
    <div v-if="user.id" class="qi-profile">
        <div class="row">
            <div class="col-sm-4">
                <p class="text-center">
                    <img height="256" width="256" class="avatar" :src="'/api/users/'+user.id+'/avatar'">
                </p>
            </div>

            <div class="col-sm-8">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h1 class="panel-title">{{user.display}}</h1>
                    </div>

                    <div class="panel-body">
                        <div class="row">
                            <div class="col-xs-6">{{$t('user_detail.member_since')}}</div>
                            <div class="col-xs-6">{{moment(user.created_at).format('YYYY-MM-DD HH:mm')}}</div>
                        </div>

                        <div class="row">
                            <div class="col-xs-6">{{$t('user_detail.last_activity')}}</div>
                            <div class="col-xs-6">
                                <span v-if="user.is_online" class="text-success">{{$t('user_detail.online')}}</span>
                                <span v-else>
                                    <span v-if="user.last_activity_at"
                                          title="{{moment(user.last_activity_at).format('YYYY-MM-DD HH:mm')}}">
                                        {{moment(user.last_activity_at).fromNow()}}
                                    </span>
                                    <span v-else>-</span>
                                </span>
                            </div>
                        </div>

                        <div class="row">
                            <div class="col-xs-6">{{$t('user_detail.rank')}}</div>
                            <div class="col-xs-6">
                                <qi-rating-rank :rating="user.rating"></qi-rating-rank>
                                ({{user.rating.toFixed(2)}})
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">{{$t('user_detail.games')}}</h3>
            </div>

            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th>{{$t('game.white')}}</th>
                        <th>{{$t('game.black')}}</th>
                        <th>{{$t('game.result')}}</th>
                        <th>{{$t('game.date')}}</th>
                        <th>&nbsp;</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="game in games">
                        <template v-if="game.is_demo">
                            <td>{{$t('game.demo')}}</td>
                            <td>{{game.demo_title}}</td>
                        </template>
                        <template v-else>
                            <td :class="{winner: game.result.startsWith('W+')}">
                                <qi-user-context :user_id="game.white_user_id" :display="game.white_display" :rating="game.rating_white"></qi-user-context>
                            </td>
                            <td :class="{winner: game.result.startsWith('B+')}">
                                <qi-user-context :user_id="game.black_user_id" :display="game.black_display" :rating="game.rating_black"></qi-user-context>
                            </td>
                        </template>
                        <td>{{game.result || '-'}}</td>
                        <td>{{moment(game.created_at).format('YYYY-MM-DD HH:mm')}}</td>
                        <td>
                            <a v-link="{name:'game', params:{game_id:game.id}}"><i class="fa fa-file"></i></a>
                            &nbsp;&nbsp;&nbsp;
                            <a :href="'/api/games/'+game.id+'/sgf'" target="_blank"><i class="fa fa-download"></i></a>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    import moment from 'moment';
    import * as socket from '../../socket';

    export default {
        mixins: [require('./../../mixins/title.vue')],

        data() {
            return {
                user: {},
                games: []
            }
        },

        route: {
            canReuse: false
        },

        ready() {
            socket.send('users/profile', {'user_id': this.user_id}, function(data) {
                this.user = data;
            }.bind(this));

            socket.send('users/games', {'user_id': this.user_id}, function(data) {
                this.games = data;
            }.bind(this));
        },

        computed: {
            window_title() {
                return this.user.user_id;
            },

            user_id() {
                return this.$route.params.user_id;
            }
        },

        methods: {
            moment
        }
    }
</script>