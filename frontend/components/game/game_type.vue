<template>
    <span>
        <template v-if="game.is_demo">{{$t('game.demo')}}</template>
        <template v-else>
            <template v-if="game.is_ranked">{{$t('game.ranked')}}</template>
            <template v-else>
                <template v-if="game.is_private">{{$t('game.private')}}</template>
                <template v-else>{{$t('game.free')}}</template>
            </template>
        </template>
    </span>
</template>

<script>
    export default {
        props: ['game']
    }
</script>
