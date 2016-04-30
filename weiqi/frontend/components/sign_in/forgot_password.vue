<template>
    <div>
        <template v-if="!sent">
            <validator name="reset">
                <form @submit.prevent="resetPassword" novalidate>
                    <div class="form-group" :class="form_group_classes($reset.email)">
                        <input type="email" class="form-control input-lg"
                               placeholder="{{$t('forgot_password.email')}}"
                               v-model="email"
                               v-validate:email="{required: true, email: true}">

                        <span class="fa fa-user form-control-feedback"></span>
                    </div>

                    <button type="submit" class="btn btn-lg btn-block btn-success" :disabled="!$reset.valid">
                        {{$t('forgot_password.reset')}}
                    </button>
                </form>
            </validator>
        </template>
        <template v-else>
            <p>
                {{$t('forgot_password.instructions')}}
            </p>
        </template>
    </div>
</template>

<script>
    export default {
        mixins: [require('../../mixins/forms.vue')],

        data() {
            return {
                sent: false,
                email: ''
            }
        },

        methods: {
            resetPassword() {
                this.$http.post('/api/auth/password-reset', {email: this.email}).then(function() {
                    this.sent = true;
                }.bind(this));
            }
        }
    }
</script>
