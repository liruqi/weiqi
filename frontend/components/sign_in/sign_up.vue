<template>
    <validator name="signUp">
        <form @submit.prevent="signUp" novalidate>
            <label>{{$t('signUp.userInfo')}}</label>

            <div class="form-group" :class="formGroupClasses($signUp.display)">
                <input type="text" class="form-control"
                       placeholder="{{$t('signUp.display')}}"
                       v-model="display"
                       v-validate:display="{required: true,
                            display_name:{rule: true, initial: 'off'}}"
                       autofocus>

                <p class="help-block">{{$t('signUp.displayHelp')}}</p>
                <p class="help-block" v-if="$signUp.display.display_name">{{$t('signUp.displayInvalid')}}</p>
            </div>

            <div class="form-group" :class="formGroupClasses($signUp.email)">
                <input type="email" class="form-control"
                       placeholder="{{$t('signUp.email')}}"
                       v-model="email"
                       v-validate:email="{required: true, email: true, emailExists:{rule: true, initial: 'off'}}">

                <p class="help-block" v-if="$signUp.email.emailExists">{{$t('signUp.emailExists')}}</p>
            </div>

            <div class="form-group" :class="formGroupClasses($signUp.password)">
                <input type="password" class="form-control"
                       placeholder="{{$t('signUp.password')}}"
                       v-model="password"
                       v-validate:password="['required']">
            </div>

            <div class="form-group">
                <label for="rank">
                    {{$t('signUp.rank.header')}}
                </label>
                <select id="rank" class="form-control" v-model="rank">
                    <option value="20k">{{$t('signUp.rank.r20k')}}</option>
                    <option value="19k">{{$t('signUp.rank.r19k')}}</option>
                    <option value="18k">{{$t('signUp.rank.r18k')}}</option>
                    <option value="17k">{{$t('signUp.rank.r17k')}}</option>
                    <option value="16k">{{$t('signUp.rank.r16k')}}</option>
                    <option value="15k">{{$t('signUp.rank.r15k')}}</option>
                    <option value="14k">{{$t('signUp.rank.r14k')}}</option>
                    <option value="13k">{{$t('signUp.rank.r13k')}}</option>
                    <option value="12k">{{$t('signUp.rank.r12k')}}</option>
                    <option value="11k">{{$t('signUp.rank.r11k')}}</option>
                    <option value="10k">{{$t('signUp.rank.r10k')}}</option>
                    <option value="9k">{{$t('signUp.rank.r9k')}}</option>
                    <option value="8k">{{$t('signUp.rank.r8k')}}</option>
                    <option value="7k">{{$t('signUp.rank.r7k')}}</option>
                    <option value="6k">{{$t('signUp.rank.r6k')}}</option>
                    <option value="5k">{{$t('signUp.rank.r5k')}}</option>
                    <option value="4k">{{$t('signUp.rank.r4k')}}</option>
                    <option value="3k">{{$t('signUp.rank.r3k')}}</option>
                    <option value="2k">{{$t('signUp.rank.r2k')}}</option>
                    <option value="1k">{{$t('signUp.rank.r1k')}}</option>
                    <option value="1d">{{$t('signUp.rank.r1d')}}</option>
                    <option value="2d">{{$t('signUp.rank.r2d')}}</option>
                    <option value="3d">{{$t('signUp.rank.r3d')}}</option>
                </select>
            </div>

            <div class="form-group">
                <label>{{$t('signUp.recaptcha')}}</label>
                <qi-recaptcha></qi-recaptcha>
            </div>

            <button type="submit" class="btn btn-lg btn-block btn-success" :disabled="!$signUp.valid || recaptcha==''">
                {{$t('signUp.signUp')}}
            </button>
        </form>
    </validator>
</template>

<script>
    import Vue from 'vue';

    export default {
        mixins: [require('../../mixins/forms.vue')],

        data() {
            return {
                'display': '',
                'email': '',
                'password': '',
                'rank': '20k',
                'recaptcha': ''
            }
        },

        validators: {
            emailExists(email) {
                return Vue.http.post('/api/auth/email-exists', {email: email}).then(function(res) {
                    if(res.data === false) {
                        return Promise.resolve();
                    } else {
                        return Promise.reject();
                    }
                }, function() {
                    return Promise.reject();
                });
            }
        },

        methods: {
            signUp() {
                var data = {
                    display: this.display,
                    email: this.email,
                    password: this.password,
                    rank: this.rank,
                    recaptcha: this.recaptcha
                };

                this.$http.post('/api/auth/sign-up', data).then(function() {
                    document.location.reload();
                }, function() {});
            }
        },

        events: {
            'recaptcha-response': function(resp) {
                this.recaptcha = resp;
            }
        }
    }
</script>
