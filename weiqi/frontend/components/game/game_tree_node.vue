<template>
    <div id="game-nav-node-{{node.id}}">
        <span class="game-nav-node-plus-minus" v-if="children.length>1 || (!isSingle && children.length>=1)" @click="toggleNode">
            <i v-if="isExpanded" class="fa fa-minus-square-o fa-fw"></i>
            <i v-else class="fa fa-plus-square-o fa-fw"></i>
        </span>
        <span v-else class="game-nav-node-plus-minus">
            <i class="fa fa-fw"></i>
        </span>

        <span class="game-nav-node-label" @click="navigate(node.id)" @dblclick="toggleNode" :class="{active: isActive}">
            <i v-if="color=='white'" class="fa fa-circle-thin"></i>
            <i v-else class="fa fa-circle"></i>
            {{moveNr}}
        </span>

        <template v-if="children.length==1 && isSingle">
            <qi-game-tree-node :game="game" :active-node="activeNode" :node="children[0]" :move-nr="moveNr+1"
                    :expanded.sync="expanded"></qi-game-tree-node>
        </template>

        <template v-if="children.length>1 || (!isSingle && children.length>=1)">
            <div class="game-nav-node collapse" :class="{in: isExpanded}">
                <template v-for="child in children">
                    <qi-game-tree-node :game="game" :active-node="activeNode" :node="child" :move-nr="moveNr+1"
                            :expanded.sync="expanded"></qi-game-tree-node>
                </template>
            </div>
        </template>
    </div>
</template>

<script>
    export default {
        name: 'qi-game-tree-node',
        props: ['game', 'activeNode', 'node', 'moveNr', 'expanded'],

        computed: {
            color() {
                if(this.node.action == 'W' || this.node.action == 'AW') {
                    return 'white';
                }
                return 'black';
            },

            children() {
                var children = [];

                (this.node.Children || []).forEach(function(child) {
                    children.push(this.game.board.tree[child]);
                }.bind(this));

                return children;
            },

            isSingle() {
                if(this.node.parent_id < 0 || !this.game.board.tree) {
                    return true;
                }

                return this.game.board.tree[this.node.parent_id].Children.length < 2;
            },

            isExpanded() {
                return this.node && !!this.expanded['n' + this.node.id];
            },

            isActive() {
                if(!this.activeNode) {
                    return false;
                }

                return this.activeNode.id == this.node.id;
            }
        },

        methods: {
            navigate(nodeID) {
                this.$dispatch('game-tree-node', nodeID);
            },

            toggleNode() {
                if(!this.node) {
                    return;
                }

                // Keys cannot begin with a number, so prefix with 'n'
                var nodeID = 'n' + this.node.id;
                this.$set('expanded.'+nodeID, !this.expanded[nodeID]);
            }
        }
    }
</script>