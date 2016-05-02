<template>
    <div>
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
                <img :src="'/api/users/' + user_id + '/avatar'" class="avatar">
            </p>
            <p class="text-center">
                <i v-if="color=='white'" class="fa fa-circle-thin"></i>
                <i v-else class="fa fa-circle"></i>
                &nbsp;&nbsp;
                <qi-user-context :user_id="user_id" :display="display" :rating="rating"></qi-user-context>
            </p>
            <p class="text-center" v-if="stage=='playing'">
                {{time}}
            </p>
            <p class="text-center" data-bind="visible: game().stage!='playing'">
                <span data-bind="text: whitePoints()"></span>
            </p>
        </template>
    </div>
</template>

<script>
    export default {
        props: ["demo", "stage", "color", "display", "user_id", "rating", "time", "points"]
    }
</script>