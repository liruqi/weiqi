<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">{{$t('settings.password.change')}}</h3>
        </div>

        <validator name="pw">
            <form @submit.prevent="save" novalidate>
                <div class="panel-body">
                    <div class="form-group has-feedback" :class="form_group_classes($pw.password)">
                        <input class="form-control" type="password"
                               v-model="password"
                               v-validate:password="['required']"
                               placeholder="{{$t('settings.password.new')}}">
                    </div>
                    <div class="form-group has-feedback" :class="form_group_classes($pw.confirm)">
                        <input class="form-control" type="password"
                                v-model="confirm"
                               v-validate:confirm="{required: true, confirm: password}"
                                placeholder="{{$t('settings.password.new_confirm')}}">
                    </div>
                </div>
                <div class="panel-footer">
                    <button type="submit" class="btn btn-success" :disabled="!$pw.valid">{{$t('settings.save')}}</button>
                </div>
            </form>
        </validator>
    </div>
</template>

<script>
    import toastr from 'toastr';
    import * as socket from '../../socket';

    export default {
        mixins: [require('../../mixins/forms.vue')],

        data() {
            return {
                password: '',
                confirm: ''
            }
        },

        validators: {
            confirm: function(val, target) {
                return val === target;
            }
        },

        methods: {
            save() {
                socket.send('settings/change_password', {password: this.password}, function() {
                    this.password = '';
                    this.confirm = '';

                    this.$nextTick(function() {
                        this.$resetValidation();
                    });

                    toastr.success(this.$t('settings.password.saved'), this.$t('general.success'));
                }.bind(this));
            }
        }
    }
</script>
