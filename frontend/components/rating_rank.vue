<template>{{rank}}</template>

<script>
    export default {
        props: ['rating'],

        computed: {
            rank() {
                var perRank = 100;
                var start = 100;
                var minRank = -20;
                var maxRank = 9;

                var rank = minRank + Math.floor((this.rating-start)/perRank);

                if(rank >= 0) {
                    rank++;
                }

                rank = Math.min(maxRank, rank);
                rank = Math.max(minRank, rank);

                if(rank > 0) {
                    return rank + "d";
                }

                return Math.abs(rank) + "k";
            }
        }
    }
</script>