<template>
    <div id="game-nav-node-{{node.id}}">
        <span class="game-nav-node-plus-minus" v-if="children.length>1 || (!is_single && children.length>=1)" @click="toggle_node">
            <i v-if="is_expanded" class="fa fa-minus-square-o fa-fw"></i>
            <i v-else class="fa fa-plus-square-o fa-fw"></i>
        </span>
        <span v-else class="game-nav-node-plus-minus">
            <i class="fa fa-fw"></i>
        </span>

        <span class="game-nav-node-label" @click="navigate(node.id)" @dblclick="toggle_node" :class="{active: is_active}">
            <i v-if="color=='white'" class="fa fa-circle-thin"></i>
            <i v-else class="fa fa-circle"></i>
            {{move_nr}}
        </span>

        <template v-if="children.length==1 && is_single">
            <qi-game-tree-node :game="game" :active_node="active_node" :node="children[0]" :move_nr="move_nr+1"
                    :expanded.sync="expanded"></qi-game-tree-node>
        </template>

        <template v-if="children.length>1 || (!is_single && children.length>=1)">
            <div class="game-nav-node collapse" :class="{in: is_expanded}">
                <template v-for="child in children">
                    <qi-game-tree-node :game="game" :active_node="active_node" :node="child" :move_nr="move_nr+1"
                            :expanded.sync="expanded"></qi-game-tree-node>
                </template>
            </div>
        </template>
    </div>
</template>

<script>
    export default {
        name: 'qi-game-tree-node',
        props: ['game', 'active_node', 'node', 'move_nr', 'expanded'],

        computed: {
            color() {
                if(this.node.action == 'W' || this.node.action == 'AW') {
                    return 'white';
                }
                return 'black';
            },

            children() {
                var children = [];

                (this.node.children || []).forEach(function(child) {
                    children.push(this.game.board.tree[child]);
                }.bind(this));

                return children;
            },

            is_single() {
                if(this.node.parent_id === null || !this.game.board.tree) {
                    return true;
                }

                return this.game.board.tree[this.node.parent_id].children.length < 2;
            },

            is_expanded() {
                return this.node && !!this.expanded['n' + this.node.id];
            },

            is_active() {
                if(!this.active_node) {
                    return false;
                }

                return this.active_node.id == this.node.id;
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
                var node_id = 'n' + this.node.id;
                this.$set('expanded.'+node_id, !this.expanded[node_id]);
            }
        }
    }
</script>