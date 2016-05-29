<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">{{$t('settings.info.header')}}</h3>
        </div>

        <validator name="settings">
            <form @submit.prevent="save" novalidate>
                <div class="panel-body">
                    <div class="form-group has-feedback" :class="form_group_classes($settings.email)">
                        <input class="form-control" type="email"
                                v-model="email"
                                v-validate:email="{required: true, email: true, email_exists:{rule: true, initial: 'off'}}"
                                placeholder="{{$t('settings.info.email')}}">

                        <p class="help-block text-danger" v-if="$settings.email.email_exists">{{$t('sign_up.email_exists')}}</p>
                    </div>
                </div>
                <div class="panel-footer">
                    <button type="submit" class="btn btn-success" :disabled="!$settings.valid">{{$t('settings.save')}}</button>
                </div>
            </form>
        </validator>
    </div>
</template>

<script>
    import Vue from 'vue';
    import * as socket from '../../socket';

    export default {
        mixins: [require('../../mixins/forms.vue')],

        data() {
            return {
                savedEmail: '',
                email: '',
            }
        },

        ready() {
            socket.send('settings/user_info', {}, function(data) {
                this.email = data.email;
                this.savedEmail = data.email;

                this.$nextTick(function() {
                    this.$resetValidation();
                });
            }.bind(this));
        },

        validators: {
            email_exists(email) {
                if(email == this.vm.savedEmail) {
                    return true;
                }

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
            save() {
                var data = {
                    email: this.email
                };

                socket.send('settings/save_user_info', data, function() {
                    this.$nextTick(function() {
                        this.$resetValidation();
                    });
                }.bind(this));
            }
        }
    }
</script>
