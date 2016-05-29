<template>
    <span v-if="!rating">{{display}}</span>
    <span v-else>{{display}} (<qi-rating-rank :rating="rating"></qi-rating-rank>)</span>
</template>

<script>
    export default {
        props: ['display', 'rating'],
    }
</script>