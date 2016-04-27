<template>
    <div>
        <h1>{{$t('passwordResetConfirm.header')}}</h1>

        <p v-if="$route.params.status=='sent'">
            {{$t('passwordResetConfirm.sent')}}
        </p>
        <p v-else>
            {{$t('passwordResetConfirm.failed')}}
        </p>
    </div>
</template>

<script>
    export default {}
</script>