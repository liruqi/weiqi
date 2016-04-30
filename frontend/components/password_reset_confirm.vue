<template>
    <div>
        <h1>{{$t('password_reset_confirm.header')}}</h1>

        <p v-if="$route.params.status=='sent'">
            {{$t('password_reset_confirm.sent')}}
        </p>
        <p v-else>
            {{$t('password_reset_confirm.failed')}}
        </p>
    </div>
</template>

<script>
    export default {}
</script>