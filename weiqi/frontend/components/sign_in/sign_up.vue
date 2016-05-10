<template>
    <template v-if="submitted">
        <p>
            {{$t('sign_up.confirm_email')}}
        </p>
    </template>
    <template v-else>
        <validator name="sign_up">
            <form @submit.prevent="sign_up" novalidate>
                <label>{{$t('sign_up.user_info')}}</label>

                <div class="form-group" :class="form_group_classes($sign_up.display)">
                    <input type="text" class="form-control"
                           placeholder="{{$t('sign_up.display')}}"
                           v-model="display"
                           v-validate:display="{required: true,
                                display_name:{rule: true, initial: 'off'}}"
                           autofocus>

                    <p class="help-block">{{$t('sign_up.display_help')}}</p>
                    <p class="help-block" v-if="$sign_up.display.display_name">{{$t('sign_up.display_invalid')}}</p>
                </div>

                <div class="form-group" :class="form_group_classes($sign_up.email)">
                    <input type="email" class="form-control"
                           placeholder="{{$t('sign_up.email')}}"
                           v-model="email"
                           v-validate:email="{required: true, email: true, email_exists:{rule: true, initial: 'off'}}">

                    <p class="help-block" v-if="$sign_up.email.email_exists">{{$t('sign_up.email_exists')}}</p>
                </div>

                <div class="form-group" :class="form_group_classes($sign_up.password)">
                    <input type="password" class="form-control"
                           placeholder="{{$t('sign_up.password')}}"
                           v-model="password"
                           v-validate:password="['required']">
                </div>

                <div class="form-group">
                    <label for="rank">
                        {{$t('sign_up.rank.header')}}
                    </label>
                    <select id="rank" class="form-control" v-model="rank">
                        <option value="20k">{{$t('sign_up.rank.r20k')}}</option>
                        <option value="19k">{{$t('sign_up.rank.r19k')}}</option>
                        <option value="18k">{{$t('sign_up.rank.r18k')}}</option>
                        <option value="17k">{{$t('sign_up.rank.r17k')}}</option>
                        <option value="16k">{{$t('sign_up.rank.r16k')}}</option>
                        <option value="15k">{{$t('sign_up.rank.r15k')}}</option>
                        <option value="14k">{{$t('sign_up.rank.r14k')}}</option>
                        <option value="13k">{{$t('sign_up.rank.r13k')}}</option>
                        <option value="12k">{{$t('sign_up.rank.r12k')}}</option>
                        <option value="11k">{{$t('sign_up.rank.r11k')}}</option>
                        <option value="10k">{{$t('sign_up.rank.r10k')}}</option>
                        <option value="9k">{{$t('sign_up.rank.r9k')}}</option>
                        <option value="8k">{{$t('sign_up.rank.r8k')}}</option>
                        <option value="7k">{{$t('sign_up.rank.r7k')}}</option>
                        <option value="6k">{{$t('sign_up.rank.r6k')}}</option>
                        <option value="5k">{{$t('sign_up.rank.r5k')}}</option>
                        <option value="4k">{{$t('sign_up.rank.r4k')}}</option>
                        <option value="3k">{{$t('sign_up.rank.r3k')}}</option>
                        <option value="2k">{{$t('sign_up.rank.r2k')}}</option>
                        <option value="1k">{{$t('sign_up.rank.r1k')}}</option>
                        <option value="1d">{{$t('sign_up.rank.r1d')}}</option>
                        <option value="2d">{{$t('sign_up.rank.r2d')}}</option>
                        <option value="3d">{{$t('sign_up.rank.r3d')}}</option>
                    </select>
                </div>

                <div class="form-group">
                    <label>{{$t('sign_up.recaptcha')}}</label>
                    <qi-recaptcha></qi-recaptcha>
                </div>

                <button type="submit" class="btn btn-lg btn-block btn-success" :disabled="!$sign_up.valid || recaptcha==''">
                    {{$t('sign_up.sign_up')}}
                </button>
            </form>
        </validator>
    </template>
</template>

<script>
    import Vue from 'vue';
    import * as socket from '../../socket';

    export default {
        mixins: [require('../../mixins/forms.vue')],

        data() {
            return {
                submitted: false,
                display: '',
                email: '',
                password: '',
                rank: '20k',
                recaptcha: ''
            }
        },

        validators: {
            email_exists(email) {
                return new Promise(function(resolve, reject) {
                    socket.send('users/email_exists', {'email': email}, function(data) {
                        if(!data) {
                            return resolve();
                        } else {
                            return reject();
                        }
                    });
                });
            }
        },

        methods: {
            sign_up() {
                var data = {
                    display: this.display,
                    email: this.email,
                    password: this.password,
                    rank: this.rank,
                    recaptcha: this.recaptcha
                };

                this.$http.post('/api/auth/sign-up', data).then(function() {
                    this.submitted = true;
                }.bind(this), function() {});
            }
        },

        events: {
            'recaptcha-response': function(resp) {
                this.recaptcha = resp;
            }
        }
    }
</script>
