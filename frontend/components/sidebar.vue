<template>
    <aside class="main-sidebar sidebar">
        <div class="user-panel">
            <div class="pull-left image">
                <a v-link="{name:'user', params:{userID:user.userID}}">
                    <img :src="user.avatarURL" class="avatar">
                </a>
            </div>
            <div class="pull-left info">
                <p>
                    <a v-link="{name:'user', params:{userID:user.userID}}">{{user.userID}}</a>
                </p>

                <span v-if="user.loggedIn">
                    <i class="fa fa-trophy"></i>
                    {{user.wins}}
                    &mdash;
                    <qi-rating-rank v-if="user.rating != null" :rating="user.rating"></qi-rating-rank>
                </span>
            </div>

            <div class="clearfix"></div>

            <div class="user-buttons">
                <button type="button" class="btn btn-success btn-block" data-toggle="modal" data-target="#qi-sign-in" v-if="!user.loggedIn">
                    {{$t('sidebar.signIn')}}
                </button>

                <div class="btn-group btn-block" v-if="user.loggedIn">
                    <template v-if="user.automatch">
                        <button type="button" class="btn btn-primary col-xs-10" @click="cancelAutomatch">
                            <i class="fa fa-spinner fa-spin"></i>&nbsp;&nbsp;
                            {{$t('sidebar.searchingAutomatch')}}
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
                                {{$t('sidebar.createDemo')}}
                            </a>
                        </li>
                        <li>
                            <a href="#" data-toggle="modal" data-target="#qi-upload-sgf">
                                {{$t('sidebar.uploadSGF')}}
                            </a>
                        </li>
                        <li><a href="#">Challenge</a></li>
                    </ul>
                </div>
            </div>
        </div>

        <ul class="sidebar-menu">
            <li v-link-active>
                <a v-link="{name:'activeGames', exact: true}">
                    <i class="fa fa-globe"></i>
                    {{$t('sidebar.activeGames')}}
                </a>
            </li>
        </ul>

        <ul class="sidebar-menu">
            <li class="header">{{$t('sidebar.games')}}</li>

            <template v-for="game in sortedGames">
                <li v-link-active>
                    <a v-link="{name: 'game', params:{gameID: game.ID}}">
                        <i :class="{'text-info': game.Stage!='finished' && !gameHasUpdate[game.ID],
                            'text-warning': game.Stage!='finished' && gameHasUpdate[game.ID]}"
                            class="fa fa-circle"></i>

                        <span v-if="game.Demo">{{game.DemoOwner}}</span>
                        <span v-else>{{game.MatchWhite}} &mdash; {{game.MatchBlack}}</span>

                        <span class="sidebar-item-action pull-right" v-if="canCloseGame(game.ID)" @click.prevent="closeGame(game.ID)">
                            <i class="fa fa-times-circle"></i>
                        </span>
                    </a>
                </li>
            </template>

            <li v-if="openGames.length == 0">
                <span class="sidebar-text">{{$t('sidebar.noGames')}}</span>
            </li>
        </ul>

        <ul class="sidebar-menu">
            <li class="header">{{$t('sidebar.rooms')}}</li>
            <template v-for="room in globalRooms">
                <li v-if="room.Type=='global'" v-link-active :class="{highlight: roomHasUpdate[room.ID]}">
                    <a v-link="{name:'room', params:{roomID: room.ID}}">
                        <i :class="{'text-info': roomHasUpdate[room.ID]}" class="fa fa-users"></i>
                        {{room.Name}}
                    </a>
                </li>
            </template>
        </ul>

        <ul class="sidebar-menu" v-if="user.loggedIn">
            <li class="header">{{$t('sidebar.people')}}</li>

            <template v-for="room in directRooms">
                <li v-link-active :class="{highlight: roomHasUpdate[room.RoomID]}">
                    <a v-link="{name:'userMessage', params:{userID:$key}}">
                        <i :class="{'text-success': room.IsOnline, 'text-info': roomHasUpdate[room.RoomID]}" class="fa fa-user"></i> {{$key}}
                    </a>
                </li>
            </template>

            <li v-if="noDirectRooms">
                <span class="sidebar-text">{{$t('sidebar.noDirectRooms')}}</span>
            </li>
        </ul>

        <hr>

        <ul class="list-inline list-unstyled text-center">
            <li>
                <a href="https://gitlab.com/mibitzi/weiqi.gs" target="_blank"><i class="fa fa-github"></i></a>
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
    import { closeGame } from '../vuex/actions';

    export default {
        vuex: {
            getters: {
                user: function(state) { return state.auth.user; },
                rooms: function(state) { return state.rooms; },
                directRooms: function(state) { return state.directRooms; },
                openGames: function(state) { return state.openGames; },
                roomHasUpdate: function(state) { return state.roomHasUpdate; },
                gameHasUpdate: function(state) { return state.gameHasUpdate; }
            },
            actions: {
                closeGame
            }
        },

        computed: {
            globalRooms() {
                return this.rooms.filter(function(room) {
                    return room.Type == 'global';
                });
            },

            sortedGames() {
                return this.openGames.sort(function(g1, g2) {
                    return g1.ID < g2.ID;
                });
            },

            noDirectRooms() {
                return !this.directRooms || Object.keys(this.directRooms).length==0
            }
        },

        methods: {
            cancelAutomatch() {
                this.$http.post('/api/play/automatch/cancel');
            },

            canCloseGame(gameID) {
                return !(this.$route.name == "game" && this.$route.params.gameID == gameID);
            }
        }
    }
</script>
