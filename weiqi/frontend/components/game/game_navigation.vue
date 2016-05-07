<template>
    <div v-show="is_visible">
        <div class="game-navigation">
            <div class="game-nav-node">
                <qi-game-tree-node v-if="has_nodes" :game="game" :active_node="current_node" :node_id="0"
                                   :move_nr="1" :expanded.sync="expanded"></qi-game-tree-node>
            </div>
        </div>

        <div class="game-nav-buttons">
            <button class="btn btn-default btn-xs" @click="first_move()">&laquo;</button>
            <button class="btn btn-default btn-xs" @click="previous_move()">&lsaquo;</button>
            <button class="btn btn-default btn-xs" @click="next_move()">&rsaquo;</button>
            <button class="btn btn-default btn-xs" @click="last_move()">&raquo;</button>
        </div>

        <button v-el:back-to-game v-if="!game.is_demo || !has_control" class="btn btn-default btn-xs btn-block" @click="back_to_game()">
            {{$t('game.back_to_game')}}
        </button>
    </div>
</template>

<script>
    import * as socket from '../../socket';

    export default {
        props: ['game', 'is_player', 'has_control', 'force_node_id'],
        components: {
            'qi-game-tree-node': require('./game_tree_node.vue')
        },

        data() {
            return {
                expanded: {}
            }
        },

        events: {
            'game-tree-node': function(node_id) {
                this.set_node_id(node_id);
            },

            'game-navigate': function(step) {
                if(this.is_player && this.game.stage != 'finished') {
                    return;
                }

                if(step > 0) {
                    this.next_move();
                } else if(step < 0) {
                    this.previous_move();
                }
            }
        },

        ready() {
            this.handle_node_change(this.current_node);
        },

        watch: {
            'current_node': function(node) {
                this.handle_node_change(node);
            }
        },

        computed: {
            is_visible() {
                return this.game.is_demo || !this.is_player || this.game.stage=='finished';
            },

            has_nodes() {
                return (this.game.board.tree || []).length > 0;
            },

            current_node() {
                if(!this.has_nodes) {
                    return null;
                }

                var node_id = this.force_node_id;

                if(node_id === false) {
                    node_id = this.game.board.current_node_id;
                }

                return this.game.board.tree[node_id];
            },
        },

        methods: {
            previous_move() {
                var node = this.current_node;

                if(node && node.parent_id !== null) {
                    this.set_node_id(node.parent_id)
                }
            },

            next_move() {
                if(!this.has_nodes) {
                    return;
                }

                var node = this.current_node;

                if(node && node.children && node.children.length > 0) {
                    this.set_node_id(node.children[0]);
                }

                if(this.force_node_id == this.game.board.current_node_id) {
                    this.force_node_id = false;
                }
            },

            first_move() {
                if(!this.has_nodes) {
                    return;
                }

                this.set_node_id(0);
            },

            last_move() {
                if(!this.has_nodes) {
                    return;
                }

                var node = this.current_node;

                while(node.children && node.children.length > 0) {
                    node = this.game.board.tree[node.children[0]];
                }

                this.set_node_id(node.id);
            },

            back_to_game() {
                this.force_node_id = false;
            },

            set_node_id(node_id) {
                if(this.game.is_demo && this.has_control) {
                    socket.send('games/set_current_node', {game_id: this.game.id, node_id: node_id});
                } else {
                    this.force_node_id = node_id;

                    if(this.force_node_id == this.game.board.current_node_id) {
                        this.force_node_id = false;
                    }
                }
            },

            handle_node_change(node) {
                if(!node || !this.game.board.tree) {
                    return;
                }

                this.expand_node_path(node);

                this.$nextTick(function() {
                    this.scroll_to_node(node);
                });
            },

            expand_node_path(node) {
                while(node.parent_id !== null) {
                    this.$set('expanded.n' + node.parent_id, true);
                    node = this.game.board.tree[node.parent_id];
                }
            },

            scroll_to_node(node) {
                var nav = jQuery('.game-navigation');
                var el = jQuery('#game-nav-node-' + node.id);
                var labelH = el.find('.game-nav-node-label').first().height();

                nav.stop();
                nav.animate({
                    scrollTop: nav[0].scrollTop + (el.offset().top - nav.offset().top) - nav.height() / 2 + labelH / 2
                });
            }
        }
    }
</script>