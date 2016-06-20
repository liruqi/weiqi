<template>
    <div class="game-player">
        <template v-if="demo">
            <p class="text-center">
                <i v-if="color=='white'" class="fa fa-circle-thin"></i>
                <i v-else class="fa fa-circle"></i>
                &nbsp;&nbsp;
                {{display}}
            </p>
        </template>

        <template v-else>
            <p class="text-center">
                <span class="avatar-wrapper">
                    <img :src="'/api/users/' + user_id + '/avatar?size=large'" class="avatar">
                </span>
            </p>
            <p class="text-center">
                <i v-if="color=='white'" class="fa fa-circle-thin"></i>
                <i v-else class="fa fa-circle"></i>
                &nbsp;&nbsp;
                <qi-user-context :user_id="user_id" :display="display" :rating="rating"></qi-user-context>
            </p>
            <p class="text-center" v-if="stage=='playing'">
                <span :class="{'game-player-low-time': is_low_time, 'game-player-very-low-time': is_very_low_time}">
                    {{formatted_time}}
                </span>
            </p>
            <p class="text-center" data-bind="visible: game().stage!='playing'">
                <span data-bind="text: whitePoints()"></span>
            </p>
        </template>
    </div>
</template>

<script>
    import { format_duration } from '../../format';
    import { play_sound } from '../../sounds';

    export default {
        props: ["demo", "stage", "color", "display", "user_id", "rating", "main_time", "points"],

        watch: {
            'is_low_time': function(val) {
                if(val) {
                    play_sound('beep');
                }
            },

            'total_seconds': function(val) {
                if(this.is_very_low_time) {
                    play_sound('count_'+val);
                }
            }
        },

        computed: {
            total_seconds() {
                return Math.ceil(this.main_time);
            },

            is_low_time() {
                return this.total_seconds <= 60;
            },

            is_very_low_time() {
                return this.total_seconds <= 10;
            },

            formatted_time() {
                return format_duration(this.total_seconds);
            }
        }
    }
</script>