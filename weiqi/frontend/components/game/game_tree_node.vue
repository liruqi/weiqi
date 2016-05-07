<template>
    <template v-if="can_collapse">
        <div id="game-nav-node-{{node_id}}">
            <span class="game-nav-node-plus-minus" @click="toggle_node">
                <i v-if="is_expanded" class="fa fa-minus-square-o fa-fw"></i>
                <i v-else class="fa fa-plus-square-o fa-fw"></i>
            </span>

            <span class="game-nav-node-label" @click="navigate(node_id)" @dblclick="toggle_node" :class="{active: is_active}">
                <i v-if="color=='white'" class="fa fa-circle-thin"></i>
                <i v-else class="fa fa-circle"></i>
                {{move_nr}}
            </span>

            <div v-if="node.children.length > 0" class="game-nav-node collapse" :class="{in: is_expanded}">
                <template v-for="child in node.children">
                    <qi-game-tree-node :game="game" :active_node="active_node" :node_id="child" :move_nr="move_nr+1"
                                       :expanded.sync="expanded"></qi-game-tree-node>
                </template>
            </div>
        </div>
    </template>
    <template v-else>
        <div id="game-nav-node-{{node_id}}">
            <span class="game-nav-node-plus-minus">
                <i class="fa fa-fw"></i>
            </span>

            <span class="game-nav-node-label" @click="navigate(node_id)" @dblclick="toggle_node" :class="{active: is_active}">
                <i v-if="color=='white'" class="fa fa-circle-thin"></i>
                <i v-else class="fa fa-circle"></i>
                {{move_nr}}
            </span>
        </div>

        <template v-if="node.children.length > 0">
            <qi-game-tree-node :game="game" :active_node="active_node" :node_id="node.children[0]" :move_nr="move_nr+1"
                               :expanded.sync="expanded"></qi-game-tree-node>
        </template>
    </template>
</template>

<script>
    export default {
        name: 'qi-game-tree-node',
        props: ['game', 'active_node', 'node_id', 'move_nr', 'expanded'],

        computed: {
            node() {
                return this.game.board.tree[this.node_id];
            },

            color() {
                if(this.node.action == 'W' || this.node.action == 'AW') {
                    return 'white';
                }
                return 'black';
            },

            is_single() {
                if(!this.game.board.tree || this.node.parent_id === null) {
                    return true;
                }

                return this.game.board.tree[this.node.parent_id].children.length < 2;
            },

            is_expanded() {
                return this.node && !!this.expanded['n' + this.node_id];
            },

            is_active() {
                if(!this.active_node) {
                    return false;
                }

                return this.active_node.id == this.node_id;
            },

            can_collapse() {
                return this.node.children.length>1 || (!this.is_single && this.node.children.length>=1);
            }
        },

        methods: {
            navigate(node_id) {
                this.$dispatch('game-tree-node', node_id);
            },

            toggle_node() {
                if(!this.node) {
                    return;
                }

                // Keys cannot begin with a number, so prefix with 'n'
                var node_id = 'n' + this.node_id;
                this.$set('expanded.'+node_id, !this.expanded[node_id]);
            }
        }
    }
</script>