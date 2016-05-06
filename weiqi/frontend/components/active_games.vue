<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <h1 class="panel-title">
                <i class="fa fa-globe fa-fw"></i>
                {{$t('gamelist.header')}}
            </h1>
        </div>

        <table class="table table-hover table-striped table-condensed gamelist">
            <thead>
                <tr>
                    <th>{{$t('game.white')}}</th>
                    <th>{{$t('game.black')}}</th>
                    <th>{{$t('game.started')}}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="game in sorted_games" v-link="{name:'game', params:{game_id: game.id}}">
                    <template v-if="game.is_demo">
                        <td colspan="2">
                            <qi-username-rank :user_id="game.demo_owner_id" :rating="game.demo_owner_rating"></qi-username-rank>
                            <span v-if="game.demo_title">&mdash; {{game.demo_title}}</span>
                        </td>
                    </template>
                    <template v-else>
                        <td>
                            <qi-username-rank :user_id="game.white_user_id" :display="game.white_display" :rating="game.white_rating"></qi-username-rank>
                        </td>
                        <td>
                            <qi-username-rank :user_id="game.black_user_id" :display="game.black_display" :rating="game.black_rating"></qi-username-rank>
                        </td>
                    </template>
                    <td>{{started[game.id]}}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>
    import Vue from 'vue';
    import moment from 'moment';

    export default {
        mixins: [require('./../mixins/title.vue')],

        data() {
            return {
                started: {},
                timer: null
            }
        },

        vuex: {
            getters: {
                active_games: function(state) { return state.active_games; }
            }
        },

        computed: {
            window_title() {
                return this.$t('gamelist.header');
            },

            sorted_games() {
                var calc_rating = function(g) {
                    if(g.Demo) {
                        return g.demo_owner_rating;
                    }
                    return Math.max(g.black_rating, g.white_rating);
                };

                return this.active_games.slice().sort(function(a, b) {
                    return calc_rating(b) - calc_rating(a);
                });
            }
        },

        ready() {
            this.update_timing();
            this.timer = setInterval(this.update_timing, 10*1000);
        },

        destroyed() {
            clearInterval(this.timer);
        },

        methods: {
            update_timing() {
                this.active_games.forEach(function(game) {
                    Vue.set(this.started, game.id, moment(game.created_at).fromNow());
                }.bind(this));
            }
        }
    }
</script>