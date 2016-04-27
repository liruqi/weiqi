<template>
    <span v-if="!rating">{{userID}}</span>
    <span v-else>{{userID}} (<qi-rating-rank :rating="rating"></qi-rating-rank>)</span>
</template>

<script>
    export default {
        props: ['userID', 'rating'],
    }
</script>