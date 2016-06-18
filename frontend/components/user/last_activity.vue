<template>
    <span v-if="user.is_online" class="text-success">{{$t('user.online')}}</span>
    <span v-else>
        <span v-if="user.last_activity_at" title="{{format_datetime(user.last_activity_at)}}">
            {{format_from_now(user.last_activity_at)}}
        </span>
        <span v-else>-</span>
    </span>
</template>
<script>
    import { format_datetime, format_from_now } from '../../format';

    export default {
        props: ['user'],

        methods: {
            format_datetime: format_datetime,
            format_from_now: format_from_now
        }
    }
</script>