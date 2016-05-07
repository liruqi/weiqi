<template>
    <div class="game-move-tree game-move-tree-{{parent_id}}" v-if="parent_id === false || is_expanded(parent_id)">
        <template v-for="(move_index, move) in move_tree">
            <template v-if="move.type == 'node'">
                <div id="game-nav-node-{{move.node_id}}" class="game-nav-node">
                    <span class="game-nav-node-plus-minus" @click="toggle_node(move.node_id)">
                        <template v-if="move.can_collapse">
                            <i v-if="is_expanded(move.node_id)" class="fa fa-minus-square-o fa-fw"></i>
                            <i v-else class="fa fa-plus-square-o fa-fw"></i>
                        </template>
                        <template v-else>
                            <i class="fa fa-fw"></i>
                        </template>
                    </span>

                    <span class="game-nav-node-label"
                          @click="navigate(move.node_id)"
                          @dblclick="toggle_node(move.node_id)"
                          :class="{active: active_node.id==move.node_id}">
                        <i v-if="color(move.node_id)=='white'" class="fa fa-circle-thin"></i>
                        <i v-else class="fa fa-circle"></i>
                        {{move_index + move_nr_start}}
                    </span>
                </div>
            </template>
            <template v-else>
                <template v-for="var in move.vars">
                    <qi-game-tree :game="game"
                                  :move_tree="var"
                                  :move_nr_start="move_index + move_nr_start"
                                  :active_node="active_node"
                                  :expanded.sync="expanded"
                                  :parent_id="move.parent_id">
                    </qi-game-tree>
                </template>
            </template>
        </template>
    </div>
</template>

<script>
    export default{
        name: 'qi-game-tree',
        props: ['game', 'move_tree', 'move_nr_start', 'active_node', 'expanded', 'parent_id'],

        methods: {
            color(node_id) {
                var node = this.game.board.tree[node_id];
                if(node.action == 'W' || node.action == 'AW') {
                    return 'white';
                }
                return 'black';
            },

            is_expanded(node_id) {
                return !!this.expanded['n' + node_id];
            },

            toggle_node(node_id) {
                // Keys cannot begin with a number, so prefix with 'n'
                node_id = 'n' + node_id;
                this.$set('expanded.'+node_id, !this.expanded[node_id]);
            },

            navigate(node_id) {
                this.$dispatch('game-tree-node', node_id);
            },
        }
    }
</script>