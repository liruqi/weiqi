<template>
    <div v-if="user.user_id" class="qi-profile">
        <div class="row">
            <div class="col-sm-4 col-sm-push-8">
                <p class="text-center">
                    <img height="256" width="256" class="avatar" :src="'/api/users/'+user.user_id+'/avatar'">
                </p>
            </div>

            <div class="col-sm-8 col-sm-pull-4">
                <div class="panel panel-default">
                    <div class="panel-heading">
                        <h1 class="panel-title">{{user.user_id}}</h1>
                    </div>

                    <div class="panel-body">
                        <div class="row">
                            <div class="col-xs-6">{{$t('userDetail.memberSince')}}</div>
                            <div class="col-xs-6">{{moment(user.created_at).format('YYYY-MM-DD HH:mm')}}</div>
                        </div>

                        <div class="row">
                            <div class="col-xs-6">{{$t('userDetail.rank')}}</div>
                            <div class="col-xs-6">
                                <qi-rating-rank :rating="user.Rating"></qi-rating-rank>
                                ({{user.Rating.toFixed(2)}})
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <div class="panel panel-default">
            <div class="panel-heading">
                <h3 class="panel-title">{{$t('userDetail.games')}}</h3>
            </div>

            <table class="table table-hover table-striped">
                <thead>
                    <tr>
                        <th>{{$t('game.white')}}</th>
                        <th>{{$t('game.black')}}</th>
                        <th>{{$t('game.result')}}</th>
                        <th>{{$t('game.size')}}</th>
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
                            <td :class="{winner: game.Result.startsWith('W+')}">
                                <qi-user-context :user_id="game.White" :rating="game.WhiteRating"></qi-user-context>
                            </td>
                            <td :class="{winner: game.Result.startsWith('B+')}">
                                <qi-user-context :user_id="game.Black" :rating="game.BlackRating"></qi-user-context>
                            </td>
                        </template>
                        <td>{{game.Result || '-'}}</td>
                        <td>{{game.Size}}x{{game.Size}}</td>
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
            this.$http.get('/api/users/' + this.$route.params.user_id).then(function(data) {
                this.user = data.data;
            }.bind(this), function() {});

            this.$http.get('/api/users/' + this.$route.params.user_id + '/games').then(function(data) {
                this.games = data.data;
            }.bind(this), function() {});
        },

        computed: {
            window_title() {
                return this.user.user_id;
            }
        },

        methods: {
            moment
        }
    }
</script>