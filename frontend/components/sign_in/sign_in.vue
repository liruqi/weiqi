<template>
    <div id="qi-sign-in" class="modal fade">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h4 class="modal-title">
                        {{(stage=='signIn' ? $t('signIn.header') :
                            (stage=='signUp' ? $t('signUp.header') : $t('forgotPassword.header')))}}
                    </h4>
                </div>

                <div class="modal-body signin-dialog">
                    <template v-if="stage=='signIn'">
                        <p v-if="loginFailed" class="text-danger">
                            {{$t('signIn.error')}}
                        </p>

                        <form @submit.prevent="signIn" novalidate>
                            <div class="form-group has-feedback" :class="{'has-error': loginFailed}">
                                <input class="form-control input-lg" type="text" v-model="user" required autofocus
                                    placeholder="{{$t('signIn.usernameEmail')}}">
                                <span class="fa fa-user form-control-feedback"></span>
                            </div>

                            <div class="form-group has-feedback" :class="{'has-error': loginFailed}">
                                <input class="form-control input-lg" type="password" v-model="password" required
                                    placeholder="{{$t('signIn.password')}}">
                                <span class="fa fa-lock form-control-feedback"></span>
                            </div>

                            <button type="submit" class="btn btn-lg btn-block btn-success" :disabled="signingIn">
                                <i v-if="signingIn" class="fa fa-spinner fa-spin"></i>
                                <span v-else>{{$t('signIn.signIn')}}</span>
                            </button>

                            <br/>

                            <p class="text-center">
                                <a href="javascript:void(0)" @click="stage='forgotPassword'">
                                    {{$t('signIn.forgot')}}
                                </a>
                            </p>

                            <div class="signup-or-separator">
                                <h6 class="text">{{$t('signIn.or')}}</h6>
                                <hr>
                            </div>

                            <button type="button" class="btn btn-lg  btn-block btn-info" @click="stage='signUp'">
                                {{$t('signIn.newAccount')}}
                            </button>
                        </form>
                    </template>

                    <template v-if="stage=='signUp'">
                        <qi-sign-up></qi-sign-up>
                    </template>

                    <template v-if="stage=='forgotPassword'">
                        <qi-forgot-password></qi-forgot-password>
                    </template>

                    <template v-if="stage=='passwordReset'">
                        <qi-pasword-reset></qi-pasword-reset>
                    </template>
                </div>

                <div class="modal-footer">
                    <button class="btn btn-default" data-dismiss="modal">
                        {{$t('signIn.cancel')}}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import { showModalSignIn, hideModalSignIn } from './../../vuex/actions';

    export default {
        data() {
            return {
                stage: 'signIn',
                user: '',
                password: '',
                loginFailed: false
            }
        },

        ready() {
            jQuery('#qi-sign-in').on('hidden.bs.modal', () => {
                this.stage = 'signIn';
            });
        },

        methods: {
            signIn() {
                this.loginFailed = false;

                this.$http.post('/api/auth/sign-in', {user: this.user, password: this.password}).then(function() {
                    document.location.reload();
                }, function() {
                    this.loginFailed = true;
                });
            }
        },

        components: {
            'qi-sign-up': require('./sign_up.vue'),
            'qi-forgot-password': require('./forgot_password.vue')
        }
    }
</script>
