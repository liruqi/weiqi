<template>
    <span>
        <template v-if="game.is_correspondence">{{$t('game.correspondence')}}</template>
        <template v-else>{{$t('game.live')}}</template>
    </span>
</template>

<script>
    export default {
        props: ['game']
    }
</script>
