<template>
    <div id="qi-challenge" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">
                        {{$t('challenge.dialog.header')}}
                        <small>{{$t('challenge.dialog.subheader')}}</small>
                    </h3>
                </div>

                <div class="modal-body">
                    <div class="form-group">
                        <label for="challenge-user">{{$t('challenge.dialog.user')}}</label>
                        <select class="form-control" id="challenge-user"></select>
                    </div>

                    <div class="form-group">
                        <div class="checkbox">
                            <label>
                                <input type="checkbox" v-model="private"> {{$t('challenge.dialog.private')}}
                            </label>

                            &nbsp;&nbsp;&nbsp;

                            <label>
                                <input type="checkbox" v-model="ranked" :disabled="private"> {{$t('challenge.dialog.ranked')}}
                            </label>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="challenge-board-size">{{$t('game.board_size')}}</label>
                        <select class="form-control" id="challenge-board-size" v-model="size" :disabled="ranked">
                            <option :value="19">19x19</option>
                            <option :value="13">13x13</option>
                            <option :value="9">9x9</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="challenge-handicap">{{$t('game.handicap')}}</label>
                        <select class="form-control" id="challenge-handicap" v-model="handicap" :disabled="ranked">
                            <option value="auto">{{$t('challenge.dialog.handicap.auto')}}</option>
                            <option value="0">{{$t('challenge.dialog.handicap.none')}}</option>
                            <option value="1">{{$t('challenge.dialog.handicap.no_komi')}}</option>
                            <option value="2">2</option>
                            <option value="3">3</option>
                            <option value="4">4</option>
                            <option value="5">5</option>
                            <option value="6">6</option>
                            <option value="7">7</option>
                            <option value="8">8</option>
                            <option value="9">9</option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label>{{$t('challenge.dialog.black_white')}}</label>

                        <div class="radio">
                            <label :class="{'text-muted': !can_auto_black_white}">
                                <input type="radio" name="black_white" v-model="black_white" value="auto"
                                       :disabled="ranked || !can_auto_black_white">
                                {{$t('challenge.dialog.bw.auto')}}
                            </label>

                            &nbsp;&nbsp;&nbsp;

                            <label>
                                <input type="radio" name="black_white" v-model="black_white" value="black"
                                       :disabled="ranked">
                                {{$t('challenge.dialog.bw.black')}}
                            </label>

                            &nbsp;&nbsp;&nbsp;

                            <label>
                                <input type="radio" name="black_white" v-model="black_white" value="white"
                                       :disabled="ranked">
                                {{$t('challenge.dialog.bw.white')}}
                            </label>
                        </div>
                    </div>

                    <div class="form-group">
                        <label for="challenge-komi">{{$t('game.komi')}}</label>
                        <input type="number" step="0.5" class="form-control" id="challenge-komi" v-model="komi"
                               :disabled="ranked || black_white == 'auto'">
                    </div>

                    <div class="form-group">
                        <label>{{$t('game.speed')}}</label>
                        <div class="radio">
                            <label>
                                <input type="radio" name="speed" v-model="speed" value="live">
                                {{$t('game.live')}}
                            </label>

                            &nbsp;&nbsp;&nbsp;

                            <label>
                                <input type="radio" name="speed" v-model="speed" value="correspondence">
                                {{$t('game.correspondence')}}
                            </label>
                        </div>
                    </div>

                    <!-- TODO: No other timings implemented
                    <div class="form-group">
                        <label for="challenge-timing-system">{{$t('game.timing')}}</label>
                        <select class="form-control" id="challenge-timing-system" v-model="timing" :disabled="speed == 'correspondence'">
                            <option value="fischer">Fischer</option>
                        </select>
                    </div>
                    -->

                    <div class="form-group">
                        <label for="challenge-maintime">{{$t('game.maintime')}}</label>
                        <select class="form-control" id="challenge-maintime" v-model="maintime">
                            <option v-for="opt in maintime_options" :value="opt[0]">
                                {{opt[1]}}
                            </option>
                        </select>
                    </div>

                    <div class="form-group">
                        <label for="challenge-overtime">{{$t('game.overtime')}}</label>
                        <select class="form-control" id="challenge-overtime" v-model="overtime">
                            <option v-for="opt in fischer_options" :value="opt[0]">
                                {{opt[1]}}
                            </option>
                        </select>
                    </div>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-primary" @click="submit">
                        {{$t('challenge.dialog.submit')}}
                    </button>

                    <button class="btn btn-default" data-dismiss="modal">{{$t('challenge.dialog.cancel')}}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import * as socket from '../../socket';
    import { rating_to_rank } from '../../rating';

    export default {
        data() {
            return {
                suggestions: {},

                size: 19,
                timing: 'fischer',
                handicap: 'auto',
                komi: SETTINGS.DEFAULT_KOMI,
                black_white: 'auto',
                speed: 'live',
                maintime: 10,
                overtime: 20,
                private: false,
                ranked: false
            }
        },

        vuex: {
            getters: {
                auth_user: function (state) {
                    return state.auth.user
                }
            }
        },

        ready() {
            var select = jQuery('#challenge-user');

            // select2 has an issue if it is placed inside a bootstrap modal
            // see:
            // https://github.com/select2/select2/issues/1645
            // https://github.com/select2/select2/issues/942
            jQuery.fn.modal.Constructor.prototype.enforceFocus = function () {};

            select.select2({
                theme: 'bootstrap',
                minimumInputLength: 2,

                ajax: {
                    dataType: 'json',

                    transport: function(params, success, failure) {
                        socket.send('users/autocomplete', {query: params.data.q}, function(users) {
                            success(users);
                        });
                    },

                    processResults: function(data, params) {
                        data.forEach(function(user) {
                            user.text = this.option_text(user.display, user.rating);
                        }.bind(this));

                        if(this.auth_user.logged_in) {
                            data = data.filter(function (user) {
                                return user.id != this.auth_user.user_id;
                            }.bind(this));
                        }

                        return {
                            results: data
                        }
                    }.bind(this)
                }
            });

            select.on('qi:set_user', function(ev, user_id) {
                socket.send('play/challenge_setup_suggestion', {user_id: user_id}, function(data) {
                    select.empty().append(
                            '<option value="' + data.other_user_id + '">' +
                            this.option_text(data.other_display, data.other_rating) +
                            '</option>');

                    select.val(data.other_user_id);
                    select.select2('data')[0].rating = data.other_rating;
                    select.trigger('change');

                    this.suggestions = data;
                    this.setup_suggestions();
                }.bind(this));
            }.bind(this));

            select.change(function() {
                socket.send('play/challenge_setup_suggestion', {user_id: select.val()}, function(data) {
                    this.suggestions = data;
                    this.setup_suggestions();
                }.bind(this));
            }.bind(this));
        },

        computed: {
            can_auto_black_white() {
                return this.handicap == 'auto' || this.handicap == '0';
            },

            maintime_options() {
                if(this.speed == 'correspondence') {
                    return [
                        [24, "1d"],
                        [24*2, "2d"],
                        [24*3, "3d"],
                        [24*4, "4d"],
                        [24*5, "5d"]
                    ];
                } else {
                    return [
                        [1, "1min"],
                        [5, "5min"],
                        [10, "10min"],
                        [15, "15min"],
                        [20, "20min"],
                        [30, "30min"],
                        [40, "40min"],
                        [50, "50min"],
                        [60, "60min"]
                    ];
                }
            },

            fischer_options() {
                if(this.speed == 'correspondence') {
                    return [
                        [4, "4h"],
                        [5, "5h"],
                        [6, "6h"],
                        [7, "7h"],
                        [8, "8h"],
                        [10, "10h"],
                        [12, "12h"],
                        [16, "16h"],
                        [20, "20h"],
                        [24, "1d"],
                        [36, "1d 12h"],
                        [24*2, "2d"],
                        [24*3, "3d"]
                    ];
                } else {
                    return [
                        [10, "10sec"],
                        [15, "15sec"],
                        [20, "20sec"],
                        [30, "30sec"],
                        [40, "40sec"],
                        [50, "50sec"],
                        [60, "60sec"]
                    ];
                }
            }
        },

        watch: {
            'private': function(val) {
                if(val) {
                    this.ranked = false;
                }
            },

            'ranked': function(val) {
                if(val) {
                    this.setup_suggestions();
                }
            },

            'can_auto_black_white': function(val) {
                if(!val && this.black_white == 'auto') {
                    var selected = this.selected_user();

                    if(selected && selected.rating > this.auth_user.rating) {
                        this.black_white = 'white';
                    } else {
                        this.black_white = 'black';
                    }
                }
            },

            'handicap': function(val) {
                if(val != 'auto' && val != '0') {
                    this.komi = SETTINGS.HANDICAP_KOMI;
                } else {
                    this.komi = SETTINGS.DEFAULT_KOMI;
                }
            },

            'speed': function(val) {
                if(val == 'correspondence') {
                    this.timing = 'fischer';
                    this.maintime = 24*3;
                    this.overtime = 24;
                }
            }
        },

        methods: {
            selected_user() {
                var data = jQuery('#challenge-user').select2('data');
                if(data) {
                    return data[0];
                }
                return null;
            },

            option_text(display, rating) {
                return display + ' (' + rating_to_rank(rating) + ')';
            },

            setup_suggestions() {
                if(this.suggestions.handicap === null) {
                    this.handicap = 'auto';
                } else {
                    this.handicap = ''+this.suggestions.handicap;
                }

                if(this.suggestions.owner_is_black === null) {
                    this.black_white = 'auto';
                } else if(this.suggestions.owner_is_black) {
                    this.black_white = 'black';
                } else {
                    this.black_white = 'white';
                }

                this.komi = this.suggestions.komi;
            },

            submit() {
                var data = {
                    user_id: +jQuery('#challenge-user').val(),
                    size: this.size,
                    handicap: null,
                    komi: +this.komi,
                    owner_is_black: null,
                    speed: this.speed,
                    timing: this.timing,
                    maintime: this.maintime,
                    overtime: this.overtime,
                    overtime_count: 1,
                    private: this.private,
                    ranked: this.ranked
                };

                if(this.handicap != 'auto') {
                    data.handicap = +this.handicap;
                }

                if(this.black_white != 'auto') {
                    data.owner_is_black = (this.black_white == 'black');
                }

                socket.send('play/challenge', data, function() {
                    jQuery('#qi-challenge').modal('hide');
                });
            }
        }
    }
</script>
