<template>
    <aside class="main-sidebar sidebar">
        <div class="user-panel">
            <template v-if="user.logged_in">
                <div class="pull-left image">
                    <a v-link="{name:'user', params:{user_id:user.user_id}}">
                        <img :src="user.avatar_url" class="avatar">
                    </a>
                </div>
                <div class="pull-left info">
                    <p>
                        <a v-link="{name:'user', params:{user_id:user.user_id}}">{{user.user_display}}</a>
                    </p>

                    <span>
                        <i class="fa fa-trophy"></i>
                        {{user.wins}}
                        &mdash;
                        <qi-rating-rank v-if="user.rating != null" :rating="user.rating"></qi-rating-rank>
                    </span>
                </div>

                <div class="clearfix"></div>
            </template>

            <div class="user-buttons">
                <button type="button" class="btn btn-success btn-block" data-toggle="modal" data-target="#qi-sign-in" v-if="!user.logged_in">
                    {{$t('sidebar.sign_in')}}
                </button>

                <div class="btn-group btn-block" v-if="user.logged_in">
                    <template v-if="user.automatch">
                        <button type="button" class="btn btn-primary col-xs-10" @click="cancel_automatch">
                            <i class="fa fa-spinner fa-spin"></i>&nbsp;&nbsp;
                            {{$t('sidebar.searching_automatch')}}
                        </button>
                    </template>
                    <template v-else>
                        <button type="button" class="btn btn-primary col-xs-10" data-toggle="modal" data-target="#qi-play-dialog">
                            {{$t('sidebar.play')}}
                        </button>
                    </template>

                    <button type="button" class="btn btn-primary dropdown-toggle col-xs-2" data-toggle="dropdown">
                        <span class="caret"></span>
                    </button>

                    <ul class="dropdown-menu col-xs-12">
                        <li>
                            <a href="#" data-toggle="modal" data-target="#qi-create-demo">
                                {{$t('sidebar.create_demo')}}
                            </a>
                        </li>
                        <li>
                            <a href="#" data-toggle="modal" data-target="#qi-upload-sgf">
                                {{$t('sidebar.upload_sgf')}}
                            </a>
                        </li>
                        <li>
                            <a href="#" data-toggle="modal" data-target="#qi-challenge">
                                {{$t('sidebar.challenge')}}
                            </a>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <ul class="sidebar-menu">
            <li v-link-active>
                <a v-link="{name:'active_games', exact: true}">
                    <i class="fa fa-globe"></i>
                    {{$t('sidebar.active_games')}}
                </a>
            </li>
        </ul>

        <ul class="sidebar-menu" v-if="challenges.length > 0">
            <li class="header">{{$t('sidebar.challenges')}}</li>

            <template v-for="challenge in challenges">
                <li v-link-active>
                    <a v-link="{name: 'challenge', params: {'challenge_id': challenge.id}}">
                        <i class="fa fa-trophy"></i>

                        <span v-if="challenge.owner_id == user.user_id">{{challenge.challengee_display}}</span>
                        <span v-else>{{challenge.owner_display}}</span>

                        <!--<span class="sidebar-item-action pull-right" @click.prevent="close_challenge(challenge.id)">
                            <i class="fa fa-times-circle"></i>
                        </span>-->
                    </a>
                </li>
            </template>
        </ul>

        <ul class="sidebar-menu">
            <li class="header">{{$t('sidebar.games')}}</li>

            <template v-for="game in sorted_games">
                <li v-link-active>
                    <a v-link="{name: 'game', params:{game_id: game.id}}">
                        <i :class="{'text-info': game.stage!='finished' && !game_has_update[game.id],
                            'text-warning': game.stage!='finished' && game_has_update[game.id]}"
                            class="fa fa-circle"></i>

                        <span v-if="game.is_demo">{{game.demo_owner_display}}</span>
                        <span v-else>{{game.white_display}} &mdash; {{game.black_display}}</span>

                        <span class="sidebar-item-action pull-right" v-if="can_close_game(game.id)" @click.prevent="close_game(game.id)">
                            <i class="fa fa-times-circle"></i>
                        </span>
                    </a>
                </li>
            </template>

            <li v-if="open_games.length == 0">
                <span class="sidebar-text">{{$t('sidebar.no_games')}}</span>
            </li>
        </ul>

        <ul class="sidebar-menu">
            <li class="header">{{$t('sidebar.rooms')}}</li>
            <template v-for="room in main_rooms">
                <li v-if="room.type=='main'" v-link-active :class="{highlight: room_has_update[room.id]}">
                    <a v-link="{name:'room', params:{room_id: room.id}}">
                        <i :class="{'text-info': room_has_update[room.id]}" class="fa fa-users"></i>
                        {{room.name}}
                    </a>
                </li>
            </template>
        </ul>

        <ul class="sidebar-menu" v-if="user.logged_in">
            <li class="header">{{$t('sidebar.people')}}</li>

            <template v-for="room in direct_rooms">
                <li v-link-active :class="{highlight: room_has_update[room.room_id]}">
                    <a v-link="{name:'user_message', params:{user_id:$key}}">
                        <i :class="{'text-success': room.is_online, 'text-info': room_has_update[room.room_id]}" class="fa fa-user"></i>
                        {{room.other_display}}
                    </a>
                </li>
            </template>

            <li v-if="no_direct_rooms">
                <span class="sidebar-text">{{$t('sidebar.no_direct_rooms')}}</span>
            </li>
        </ul>

        <hr>

        <ul class="list-inline list-unstyled text-center">
            <li>
                <a href="https://gitlab.com/mibitzi/weiqi.gs" target="_blank"><i class="fa fa-gitlab"></i></a>
            </li>
            <li>
                <a href="https://www.facebook.com/weiqi.gs" target="_blank"><i class="fa fa-facebook"></i></a>
            </li>
        </ul>

        <p class="text-center">
            <small>&copy; Copyright 2016 weiqi.gs</small>
            <br><br>
        </p>
    </aside>
</template>

<script>
    import { close_game } from '../vuex/actions';
    import * as socket from '../socket';

    export default {
        vuex: {
            getters: {
                user: function(state) { return state.auth.user; },
                rooms: function(state) { return state.rooms; },
                direct_rooms: function(state) { return state.direct_rooms; },
                open_games: function(state) { return state.open_games; },
                room_has_update: function(state) { return state.room_has_update; },
                game_has_update: function(state) { return state.game_has_update; },
                challenges: function(state) { return state.challenges; }
            },

            actions: {
                close_game
            }
        },

        computed: {
            main_rooms() {
                return this.rooms.filter(function(room) {
                    return room.type == 'main';
                });
            },

            sorted_games() {
                return this.open_games.sort(function(g1, g2) {
                    return g1.id < g2.id;
                });
            },

            no_direct_rooms() {
                return !this.direct_rooms || Object.keys(this.direct_rooms).length==0
            }
        },

        methods: {
            cancel_automatch() {
                socket.send('play/cancel_automatch');
            },

            can_close_game(game_id) {
                return !(this.$route.name == "game" && this.$route.params.game_id == game_id);
            }
        }
    }
</script>
