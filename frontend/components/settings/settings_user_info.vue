<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">{{$t('settings.info.header')}}</h3>
        </div>

        <validator name="settings">
            <form @submit.prevent="save" novalidate>
                <div class="panel-body">
                    <div class="form-group has-feedback" :class="formGroupClasses($settings.email)">
                        <input class="form-control" type="email"
                                v-model="email"
                                v-validate:email="{required: true, email: true, emailExists:{rule: true, initial: 'off'}}"
                                placeholder="{{$t('settings.info.email')}}">

                        <p class="help-block text-danger" v-if="$settings.email.emailExists">{{$t('signUp.emailExists')}}</p>
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

    export default {
        mixins: [require('../../mixins/forms.vue')],

        data() {
            return {
                savedEmail: '',
                email: '',
            }
        },

        ready() {
            this.$http.get('/api/settings').then(function(resp) {
                this.email = resp.data.Email;
                this.savedEmail = resp.data.Email;

                this.$nextTick(function() {
                    this.$resetValidation();
                });
            }.bind(this), function() {});
        },

        validators: {
            emailExists(email) {
                if(email == this.vm.savedEmail) {
                    return true;
                }

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
            save() {
                var data = {
                    email: this.email
                };

                this.$http.post('/api/settings/update', data).then(function() {
                    this.$nextTick(function() {
                        this.$resetValidation();
                    });
                }.bind(this), function() {});
            }
        }
    }
</script>
