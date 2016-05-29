<template>{{rank}}</template>

<script>
    import { rating_to_rank } from '../rating';

    export default {
        props: ['rating'],

        computed: {
            rank() {
                return rating_to_rank(this.rating);
            }
        }
    }
</script>