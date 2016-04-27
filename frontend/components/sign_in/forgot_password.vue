<template>
    <div>
        <template v-if="!sent">
            <validator name="reset">
                <form @submit.prevent="resetPassword" novalidate>
                    <div class="form-group" :class="formGroupClasses($reset.email)">
                        <input type="email" class="form-control input-lg"
                               placeholder="{{$t('forgotPassword.email')}}"
                               v-model="email"
                               v-validate:email="{required: true, email: true}">

                        <span class="fa fa-user form-control-feedback"></span>
                    </div>

                    <button type="submit" class="btn btn-lg btn-block btn-success" :disabled="!$reset.valid">
                        {{$t('forgotPassword.reset')}}
                    </button>
                </form>
            </validator>
        </template>
        <template v-else>
            <p>
                {{$t('forgotPassword.instructions')}}
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
