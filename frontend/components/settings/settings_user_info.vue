<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">{{$t('settings.info.header')}}</h3>
        </div>

        <validator name="settings">
            <form @submit.prevent="save" novalidate>
                <div class="panel-body">
                    <div class="form-group has-feedback" :class="form_group_classes($settings.email)">
                        <label for="user-email">{{$t('settings.info.email')}}</label>
                        <input id="user-email" class="form-control" type="email"
                               v-model="email"
                               v-validate:email="{required: true, email: true, email_exists:{rule: true, initial: 'off'}}">

                        <p class="help-block text-danger" v-if="$settings.email.email_exists">{{$t('sign_up.email_exists')}}</p>
                    </div>
                    <div class="checkbox">
                        <label>
                            <input type="checkbox" v-model="correspondence_emails"> {{$t('settings.info.correspondence_emails')}}
                        </label>
                    </div>
                    <div class="form-group" :class="form_group_classes($settings.info_text)">
                        <label for="user-info-text">{{$t('settings.info.text')}}</label>
                        <textarea id="user-info-text" class="form-control" v-model="info_text" rows="10"
                                  v-validate:info_text="{maxlength: 10000}"></textarea>

                        <p class="help-block text-danger" v-if="$settings.info_text.maxlength">{{$t('settings.info.text_too_long')}}</p>
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
    import toastr from 'toastr';
    import * as socket from '../../socket';

    export default {
        mixins: [require('../../mixins/forms.vue')],

        data() {
            return {
                saved_email: '',
                email: '',
                correspondence_emails: false,
                info_text: ''
            }
        },

        ready() {
            socket.send('settings/user_info', {}, function(data) {
                this.email = data.email;
                this.saved_email = data.email;
                this.correspondence_emails = data.correspondence_emails;
                this.info_text = data.info_text;

                this.$nextTick(function() {
                    this.$resetValidation();
                });
            }.bind(this));
        },

        validators: {
            email_exists(email) {
                if(email == this.vm.saved_email) {
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
                    email: this.email,
                    info_text: this.info_text,
                    correspondence_emails: this.correspondence_emails
                };

                socket.send('settings/save_user_info', data, function() {
                    this.$nextTick(function() {
                        this.$resetValidation();
                    });

                    toastr.success(this.$t('settings.info.saved'), this.$t('general.success'));
                }.bind(this));
            }
        }
    }
</script>
