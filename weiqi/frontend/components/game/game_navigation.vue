<template>
    <div v-if="game.Demo || !isPlayer || game.stage=='finished'">
        <div class="game-navigation">
            <div class="game-nav-node">
                <qi-game-tree-node v-if="rootNode" :game="game" :active-node="currentNode" :node="rootNode"
                        :move-nr="1" :expanded.sync="expanded"></qi-game-tree-node>
            </div>
        </div>

        <div class="game-nav-buttons">
            <button class="btn btn-default btn-xs" @click="firstMove()">&laquo;</button>
            <button class="btn btn-default btn-xs" @click="previousMove()">&lsaquo;</button>
            <button class="btn btn-default btn-xs" @click="nextMove()">&rsaquo;</button>
            <button class="btn btn-default btn-xs" @click="lastMove()">&raquo;</button>
        </div>

        <button v-el:back-to-game v-if="!game.Demo || !hasControl" class="btn btn-default btn-xs btn-block" @click="backToGame()">
            {{$t('game.backToGame')}}
        </button>
    </div>
</template>

<script>
    export default {
        props: ['game', 'isPlayer', 'hasControl', 'force_node_id'],
        components: {
            'qi-game-tree-node': require('./game_tree_node.vue')
        },

        data() {
            return {
                expanded: {}
            }
        },

        methods: {
            previousMove() {
                var node = this.currentNode;

                if(node && node.ParentID >= 0) {
                    this.setNodeID(node.ParentID)
                }
            },

            nextMove() {
                if(!this.hasNodes) {
                    return;
                }

                var node = this.currentNode;

                if(node && node.Children && node.Children.length > 0) {
                    this.setNodeID(node.Children[0]);
                }

                if(this.force_node_id == this.game.Board.CurrentNodeID) {
                    this.force_node_id = false;
                }
            },

            firstMove() {
                if(!this.hasNodes) {
                    return;
                }

                this.setNodeID(0);
            },

            lastMove() {
                if(!this.hasNodes) {
                    return;
                }

                var node = this.currentNode;

                while(node.Children && node.Children.length > 0) {
                    node = this.game.Board.Tree[node.Children[0]];
                }

                this.setNodeID(node.id);
            },

            backToGame() {
                this.force_node_id = false;
            },

            setNodeID(nodeID) {
                if(this.game.Demo && this.hasControl) {
                    this.$http.post('/api/games/'+this.game.id+'/set-current-node', {nodeID: nodeID});
                } else {
                    this.force_node_id = nodeID;

                    if(this.force_node_id == this.game.Board.CurrentNodeID) {
                        this.force_node_id = false;
                    }
                }
            },

            handleNodeChange(node) {
                if(!node || !this.game.Board.Tree) {
                    return;
                }

                this.expandNodePath(node);

                this.$nextTick(function() {
                    this.scrollToNode(node);
                });
            },

            expandNodePath(node) {
                while(node.ParentID >= 0) {
                    this.$set('expanded.n' + node.ParentID, true);
                    node = this.game.Board.Tree[node.ParentID];
                }
            },

            scrollToNode(node) {
                var nav = jQuery('.game-navigation');
                var el = jQuery('#game-nav-node-' + node.id);
                var labelH = el.find('.game-nav-node-label').first().height();

                nav.animate({
                    scrollTop: nav[0].scrollTop + (el.offset().top - nav.offset().top) - nav.height() / 2 + labelH / 2
                });
            }
        },

        events: {
            'game-tree-node': function(nodeID) {
                this.setNodeID(nodeID);
            },

            'game-navigate': function(step) {
                if(this.isPlayer && this.game.stage != 'finished') {
                    return;
                }

                if(step > 0) {
                    this.nextMove();
                } else if(step < 0) {
                    this.previousMove();
                }
            }
        },

        ready() {
            this.handleNodeChange(this.currentNode);
        },

        watch: {
            'currentNode': function(node) {
                this.handleNodeChange(node);
            }
        },

        computed: {
            hasNodes() {
                return (this.game.Board.Tree || []).length > 0;
            },

            currentNode() {
                if(!this.hasNodes) {
                    return null;
                }

                var nodeID = this.force_node_id;

                if(nodeID === false) {
                    nodeID = this.game.Board.CurrentNodeID;
                }

                return this.game.Board.Tree[nodeID];
            },

            rootNode() {
                if(!this.hasNodes) {
                    return;
                }

                return this.game.Board.Tree[0];
            }
        }
    }
</script>