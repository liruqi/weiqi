<template>
    <div class="game-move-tree">
        <template v-for="move in move_tree">
            <template v-if="move.type == 'node'">
                <div id="game-nav-node-{{move.node_id}}" class="game-nav-node">
                    <span class="game-nav-node-plus-minus">
                        <i class="fa fa-fw"></i>
                    </span>

                    <span class="game-nav-node-label"
                          @click="navigate(move.node_id)"
                          @dblclick="toggle_node"
                          :class="{active: active_node.id==move.node_id}">
                        <i v-if="color(move.node_id)=='white'" class="fa fa-circle-thin"></i>
                        <i v-else class="fa fa-circle"></i>
                        {{$index + move_nr_start}}
                    </span>
                </div>
            </template>
            <template v-else v-for="var in move.vars">
                <qi-game-tree :game="game"
                              :move_tree="var"
                              :move_nr_start="$index + move_nr_start"
                              :active_node="active_node"
                              :expanded.sync="expanded">
                </qi-game-tree>
            </template>
        </template>
    </div>
</template>

<script>
    export default{
        name: 'qi-game-tree',
        props: ['game', 'move_tree', 'move_nr_start', 'active_node', 'expanded'],

        methods: {
            color(node_id) {
                var node = this.game.board.tree[node_id];
                if(node.action == 'W' || node.action == 'AW') {
                    return 'white';
                }
                return 'black';
            },

            toggle_node() {
            },

            navigate(node_id) {
                this.$dispatch('game-tree-node', node_id);
            }
        }
    }
</script>