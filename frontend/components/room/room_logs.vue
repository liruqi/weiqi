<template>
    <div class="panel panel-default flex-column room-logs">
        <div class="panel-heading flex-fixed">
            <h3 class="panel-title">
                <i class="fa fa-comments-o"></i>
                <span v-if="title">{{title}}</span>
                <span v-else>
                    <span v-if="room.Type=='global'">{{room.Name}}</span>
                    <span v-else>{{$t('roomLogs.chat')}}</span>
                </span>
            </h3>
        </div>

        <div class="panel-body chat flex-auto">
            <div class="item" v-for="log in roomLogs">
                <img class="avatar" :src="'/api/users/' + log.UserID + '/avatar'">

                <p class="message">
                    <span class="name">
                        <qi-user-context :user-id="log.UserID" :rating="log.Rating"></qi-user-context>

                        <small class="text-muted pull-right" title="{{moment(log.CreatedAt).format('YYYY-MM-DD HH:mm:ss')}}">
                            <i class="fa fa-clock-o"></i>
                            {{moment(log.CreatedAt).format('HH:mm')}}
                        </small>
                    </span>

                    {{log.Message}}
                </p>
            </div>
        </div>

        <div class="panel-footer flex-fixed">
            <div v-if="loggedIn">
                <form @submit.prevent="sendMessage">
                    <div class="input-group">
                        <input type="text" class="form-control" name="message"
                               v-model="message" placeholder="{{$t('roomLogs.typeMsg')}}"
                               autocomplete="off">
                        <div class="input-group-btn">
                            <button class="btn btn-success"><i class="fa fa-plus"></i></button>
                        </div>
                    </div>
                </form>
            </div>

            <span v-else>
                <a href="#" data-toggle="modal" data-target="#qi-sign-in">{{$t('roomLogs.signIn')}}</a>
                {{$t('roomLogs.toChat')}}
            </span>
        </div>
    </div>
</template>

<script>
    import moment from 'moment';
    import { clearRoomUpdate } from '../../vuex/actions';

    export default {
        props: ['roomID', 'title', 'showOnlyUserIDs'],

        data() {
            return {
                message: '',
            }
        },

        vuex: {
            getters: {
                loggedIn: function(state) { return state.auth.user.loggedIn; },
                rooms: function(state) { return state.rooms; },
                allLogs: function(state) { return state.roomLogs; },
                roomHasUpdate: function(state) { return state.roomHasUpdate; }
            },
            actions: {
                clearRoomUpdate
            }
        },

        computed: {
            room() {
                return this.rooms.find(room => { return room.ID == this.roomID; }) || {};
            },

            roomLogs() {
                var logs = this.allLogs[this.roomID] || [];

                if((this.showOnlyUserIDs || []).length > 0) {
                    logs = logs.filter(function(log) {
                        return this.showOnlyUserIDs.includes(log.UserID);
                    }.bind(this))
                }

                return logs;
            }
        },

        watch: {
            'roomLogs': function() {
                this.scrollBottom();
                this.clearRoomUpdate(this.roomID);
            },

            'roomID': function() {
                this.scrollBottom(true);
                this.clearRoomUpdate(this.roomID);
            }
        },

        ready() {
            this.scrollBottom(true);
            this.clearRoomUpdate(this.roomID);
        },

        methods: {
            sendMessage() {
                this.$http.post('/api/rooms/'+this.roomID+'/message', {
                    message: this.message
                });

                this.message = '';
            },

            scrollBottom(force) {
                var el = jQuery(this.$el).find('.chat');
                var innerHeight = el.innerHeight();
                var scrollHeight = el.prop("scrollHeight");

                if(force || el.scrollTop() + innerHeight > scrollHeight - 200) {
                    el.scrollTop(scrollHeight);
                }
            },

            moment: moment,
        }
    }
</script>