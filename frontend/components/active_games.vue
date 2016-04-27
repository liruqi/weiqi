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
                    <th>{{$t('game.size')}}</th>
                    <th>{{$t('game.started')}}</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="game in sortedGames" v-link="{name:'game', params:{gameID: game.ID}}">
                    <template v-if="game.Demo">
                        <td colspan="2">
                            <qi-username-rank :user-id="game.DemoOwner" :rating="game.DemoOwnerRating"></qi-username-rank>
                            <span v-if="game.DemoTitle">&mdash; {{game.DemoTitle}}</span>
                        </td>
                    </template>
                    <template v-else>
                        <td>
                            <qi-username-rank :user-id="game.MatchWhite" :rating="game.MatchWhiteRating"></qi-username-rank>
                        </td>
                        <td>
                            <qi-username-rank :user-id="game.MatchBlack" :rating="game.MatchBlackRating"></qi-username-rank>
                        </td>
                    </template>
                    <td>{{game.Size}}x{{game.Size}}</td>
                    <td>{{started[game.ID]}}</td>
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
                activeGames: function(state) { return state.activeGames; }
            }
        },

        computed: {
            windowTitle() {
                return this.$t('gamelist.header');
            },

            sortedGames() {
                var calcRating = function(g) {
                    if(g.Demo) {
                        return g.DemoOwnerRating;
                    }
                    return Math.max(g.MatchBlackRating, g.MatchWhiteRating);
                };

                return this.activeGames.slice().sort(function(a, b) {
                    return calcRating(b) - calcRating(a);
                });
            }
        },

        ready() {
            this.updateTiming();
            this.timer = setInterval(this.updateTiming, 10*1000);
        },

        destroyed() {
            clearInterval(this.timer);
        },

        methods: {
            updateTiming() {
                this.activeGames.forEach(function(game) {
                    Vue.set(this.started, game.ID, moment(game.CreatedAt).fromNow());
                }.bind(this));
            }
        }
    }
</script>