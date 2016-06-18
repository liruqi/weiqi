<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <h1 class="panel-title">
                <i class="fa fa-globe fa-fw"></i>
                {{$t('gamelist.header')}}
            </h1>
        </div>

        <div class="table-responsive">
            <table class="table table-hover table-striped table-condensed gamelist">
                <thead>
                    <tr>
                        <th>{{$t('game.white')}}</th>
                        <th>{{$t('game.black')}}</th>
                        <th>{{$t('game.type')}}</th>
                        <th>{{$t('game.speed')}}</th>
                        <th>{{$t('game.started')}}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="game in sorted_games" v-link="{name:'game', params:{game_id: game.id}}">
                        <template v-if="game.is_demo">
                            <td colspan="2">
                                <qi-username-rank :display="game.demo_owner_display" :rating="game.demo_owner_rating"></qi-username-rank>
                                <span v-if="game.demo_title">&mdash; {{game.demo_title}}</span>
                            </td>
                        </template>
                        <template v-else>
                            <td>
                                <qi-username-rank :display="game.white_display" :rating="game.white_rating"></qi-username-rank>
                            </td>
                            <td>
                                <qi-username-rank :display="game.black_display" :rating="game.black_rating"></qi-username-rank>
                            </td>
                        </template>
                        <td>
                            <qi-game-type :game="game"></qi-game-type>
                        </td>
                        <td>
                            <qi-game-speed :game="game"></qi-game-speed>
                        </td>
                        <td><span :title="format_datetime(game.created_at)">{{started[game.id]}}</span></td>
                    </tr>
                    <tr v-if="sorted_games.length == 0">
                        <td colspan="5" class="text-center">
                            <em>{{$t('gamelist.no_games')}}</em>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
    import Vue from 'vue';
    import { format_datetime, format_from_now } from '../format';

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
            format_datetime: format_datetime,

            update_timing() {
                this.active_games.forEach(function(game) {
                    Vue.set(this.started, game.id, format_from_now(game.created_at));
                }.bind(this));
            }
        }
    }
</script>