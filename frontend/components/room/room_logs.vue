<template>
    <div class="panel panel-default flex-column room-logs fixed-dropdowns" :class="{'room-logs-users-visible': show_users}">
        <div class="panel-heading flex-fixed">
            <h3 class="panel-title">
                <i class="fa fa-comments-o"></i>
                <span v-if="title">{{title}}</span>
                <span v-else>
                    <span v-if="room.type=='main'">{{room.name}}</span>
                    <span v-else>{{$t('room_logs.chat')}}</span>
                </span>

                <template v-if="embed_users">
                    <span  class="room-logs-users-toggle pull-right" @click="toggle_users">
                        <i class="fa fa-users"></i> ({{room_user_count}})
                    </span>
                </template>
            </h3>
        </div>

        <div class="panel-body flex-auto">
            <div class="item" :class="{'item-narrow': is_narrow}" v-for="log in room_logs">
                <img class="avatar" :src="'/api/users/' + log.user_id + '/avatar'">

                <p class="message">
                    <span class="name">
                        <qi-user-context :user_id="log.user_id" :display="log.user_display" :rating="log.user_rating"></qi-user-context>

                        <small class="text-muted pull-right" title="{{format_datetime(log.created_at)}}">
                            <i class="fa fa-clock-o"></i>
                            {{format_time(log.created_at)}}
                        </small>
                    </span>

                    {{{log.message}}}
                </p>
            </div>
        </div>

        <div class="panel-footer flex-fixed">
            <div v-if="logged_in">
                <form @submit.prevent="send_message">
                    <div class="input-group">
                        <input type="text" class="form-control" name="message"
                               v-model="message" placeholder="{{$t('room_logs.type_msg')}}"
                               autocomplete="off">
                        <div class="input-group-btn">
                            <button class="btn btn-success"><i class="fa fa-plus"></i></button>
                        </div>
                    </div>
                </form>
            </div>

            <span v-else>
                <a href="#" data-toggle="modal" data-target="#qi-sign-in">{{$t('room_logs.sign_in')}}</a>
                {{$t('room_logs.to_chat')}}
            </span>
        </div>

        <div v-if="embed_users" class="room-logs-users">
            <qi-room-users :room_id="room_id"></qi-room-users>
        </div>
    </div>
</template>

<script>
    import { format_datetime, format_time, linkify, format_coordinates } from '../../format';
    import * as socket from '../../socket';

    export default {
        props: ['room_id', 'title', 'show_only_user_ids', 'layout', 'format_coords', 'board_size', 'message',
                'embed_users'],

        data() {
            return {
                show_users: false
            }
        },

        vuex: {
            getters: {
                logged_in: function(state) { return state.auth.user.logged_in; },
                rooms: function(state) { return state.rooms; },
                all_logs: function(state) { return state.room_logs; },
                room_has_update: function(state) { return state.room_has_update; },
                room_users: function(state) { return state.room_users; }
            }
        },

        computed: {
            room() {
                return this.rooms.find(room => { return room.id == this.room_id; }) || {};
            },

            room_logs() {
                var logs = this.all_logs[this.room_id] || [];

                if((this.show_only_user_ids || []).length > 0) {
                    logs = logs.filter(function(log) {
                        return this.show_only_user_ids.includes(log.user_id);
                    }.bind(this))
                }

                logs = this.format_logs(logs);

                return logs;
            },

            is_narrow() {
                return this.layout == 'narrow';
            },

            room_user_count() {
                return (this.room_users[this.room_id] || []).length;
            }
        },

        watch: {
            'room_logs': function() {
                this.scroll_bottom();
            },

            'room_id': function() {
                this.scroll_bottom(true);
            }
        },

        ready() {
            this.scroll_bottom(true);
        },

        methods: {
            format_datetime: format_datetime,
            format_time: format_time,

            send_message() {
                socket.send('rooms/message', {'room_id': this.room_id, 'message': this.message});
                this.message = '';
            },

            scroll_bottom(force) {
                var el = jQuery(this.$el).find('.panel-body');
                var innerHeight = el.innerHeight();
                var scrollHeight = el.prop("scrollHeight");

                if(force || el.scrollTop() + innerHeight > scrollHeight - 200) {
                    el.scrollTop(scrollHeight);
                }
            },

            format_logs(logs) {
                return logs.map(function(original) {
                    // Clone to avoid double-linking
                    var log = JSON.parse(JSON.stringify(original));

                    log.message = jQuery('<div>').text(log.message).html();
                    log.message = linkify(log.message);

                    if(this.format_coords) {
                        log.message = format_coordinates(log.message, 'coord', this.board_size);
                    }

                    return log;
                }.bind(this));
            },

            toggle_users() {
                this.show_users = !this.show_users;
            }
        }
    }
</script>
