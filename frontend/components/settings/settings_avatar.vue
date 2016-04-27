<template>
    <div class="panel panel-default">
        <div class="panel-heading">
            <h3 class="panel-title">{{$t('settings.avatar.header')}}</h3>
        </div>

        <div class="box-body">
            <p class="text-center">
                <br>
                <img class="avatar" :src="user.avatarURL">
            </p>

            <p class="text-center">
                <a href="#" class="btn btn-default file-chooser">
                    <label for="avatar-input">{{$t('settings.avatar.new')}}</label>
                    <input id="avatar-input" type="file" @change="fileChosen">
                </a>
            </p>

            <p class="text-center">
                <small>
                    <a href="javascript:void(0)" @click="deleteAvatar()">
                        {{$t('settings.avatar.delete')}}
                    </a>
                </small>
            </p>
        </div>
    </div>

    <div class="modal fade" id="avatar-modal" data-keyboard="false" data-backdrop="static">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h3 class="modal-title">{{$t('settings.avatar.header')}}</h3>
                </div>
                <div class="modal-body">
                    <p>{{$t('settings.avatar.cropHelp')}}</p>
                    <img id="avatar-cropper" class="img-responsive" style="visibility: hidden;">
                </div>
                <div class="modal-footer">
                    <button class="btn btn-default" data-dismiss="modal">{{$t('settings.avatar.cancel')}}</button>
                    <button class="btn btn-primary" @click="save()">{{$t('settings.save')}}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import bootbox from 'bootbox';
    import cropper from 'cropper';
    import { reloadUserAvatar } from '../../vuex/actions';

    export default {
        vuex: {
            getters: {
                user: function(state) { return state.auth.user; }
            }, actions: {
                reloadUserAvatar
            }
        },

        methods: {
            deleteAvatar() {
                bootbox.confirm(this.$t('settings.avatar.confirmDelete'), function(res) {
                    if (res) {
                        this.$http.post('/api/settings/delete-avatar').then(function() {
                            this.reloadUserAvatar();
                        }.bind(this), function() {});
                    }
                }.bind(this));
            },

            fileChosen() {
                var file = jQuery('#avatar-input')[0].files[0];
                var fr = new FileReader();

                fr.onload = function() {
                    jQuery('#avatar-cropper').attr('src', fr.result);
                    jQuery('#avatar-modal').modal('show');
                };

                fr.readAsDataURL(file);
            },

            save() {
                var canvas = jQuery('#avatar-cropper').cropper("getCroppedCanvas", {
                    width: 256,
                    height: 256
                });

                var dataURL = canvas.toDataURL("image/png");

                this.$http.post('/api/settings/upload-avatar', {avatar: dataURL}).then(function() {
                    jQuery('#avatar-modal').modal('hide');
                    this.reloadUserAvatar();
                }.bind(this), function() {});
            },
        },

        ready() {
            jQuery('#avatar-modal').appendTo('body');

            jQuery("#avatar-modal").on('shown.bs.modal', function() {
                jQuery('#avatar-cropper').cropper({
                    responsive:         true,
                    aspectRatio:        1,
                    strict:             false,
                    dragCrop:           false,
                    movable:            false,
                    resizable:          false,
                    minContainerWidth:  300,
                    minContainerHeight: 300,
                    minCropBoxWidth:    256,
                    minCropBoxHeight:   256
                });
            }).on('hidden.bs.modal', function() {
                jQuery('#avatar-cropper').cropper('destroy');

                var input = jQuery('#avatar-input');
                input.wrap('<form>').closest('form')[0].reset();
                input.unwrap();
            })
        },

        destroyed() {
            jQuery('body > #avatar-modal').remove();
        }
    }
</script>