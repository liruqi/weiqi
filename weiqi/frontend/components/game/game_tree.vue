<template>
    <div v-el:tree></div>
</template>

<script>
    // Vue.js does not like to render a big nested tree structure like this and will perform poorly.
    // We therefore render it directly using jQuery, which will be much faster.
    export default{
        name: 'qi-game-tree',
        props: ['game', 'move_tree', 'active_node'],

        watch: {
            'move_tree_hash': function() {
                this.render_tree();
                this.expand_active_node();
            },

            'active_node': function(node) {
                jQuery('.game-nav-node-label.active').removeClass('active');
                jQuery('#game-nav-node-'+node.id+' .game-nav-node-label').addClass('active');
                this.expand_active_node();
            }
        },

        ready() {
            this.render_tree();
            this.expand_active_node();

            jQuery(this.$els.tree).on('click', '.game-nav-node-label', function(ev) {
                var node_id = jQuery(ev.target).closest('.game-nav-node').data('node_id');
                this.navigate(node_id);
            }.bind(this));

            jQuery(this.$els.tree).on('dblclick', '.game-nav-node-label', function(ev) {
                var node_id = jQuery(ev.target).closest('.game-nav-node').data('node_id');
                this.toggle_node(node_id);
            }.bind(this));

            jQuery(this.$els.tree).on('click', '.game-nav-node-plus-minus', function(ev) {
                var node_id = jQuery(ev.target).closest('.game-nav-node').data('node_id');
                this.toggle_node(node_id);
            }.bind(this));
        },

        computed: {
            move_tree_hash() {
                return JSON.stringify(this.move_tree);
            }
        },

        methods: {
            expand_active_node() {
                var node = jQuery('#game-nav-node-'+this.active_node.id);
                node.parents('.game-move-subtree').each(function(i, sub) {
                    sub = jQuery(sub);
                    if(!sub.hasClass('in')) {
                        this.toggle_node(sub.data('node_id'));
                    }
                }.bind(this));
            },

            toggle_node(node_id) {
                var sub = jQuery('#game-move-subtree-'+node_id);
                var plus_minus = sub.prev().find('.game-nav-node-plus-minus i');

                sub.toggleClass('in');

                if(plus_minus.hasClass('fa-minus-square-o')) {
                    if(sub.find('.game-nav-node-label.active').length) {
                        this.navigate(node_id);
                    }
                }

                plus_minus.removeClass('fa-minus-square-o');
                plus_minus.removeClass('fa-plus-square-o');

                if(sub.hasClass('in')) {
                    plus_minus.addClass('fa-minus-square-o');
                } else {
                    plus_minus.addClass('fa-plus-square-o');
                }
            },

            navigate(node_id) {
                this.$dispatch('game-tree-node', node_id);
            },

            render_tree() {
                var root = jQuery(this.$els.tree);
                root.empty();
                root.append(this.render_subtree(this.move_tree));
            },

            render_subtree(tree) {
                var div = jQuery('<div/>');
                div.addClass('game-move-tree');

                tree.forEach(function(move) {
                    if(move.type == 'node') {
                        div.append(this.render_node(move));
                    } else {
                        var sub = jQuery('<div/>');
                        sub.addClass('game-move-subtree');
                        sub.addClass('collapse');
                        sub.attr('id', 'game-move-subtree-'+move.parent_id);
                        sub.data('node_id', move.parent_id);

                        move.vars.forEach(function(v) {
                            sub.append(this.render_subtree(v));
                        }.bind(this));

                        div.append(sub);
                    }
                }.bind(this));

                return div;
            },

            render_node(move) {
                var node = jQuery('<div/>');

                node.addClass('game-nav-node');
                node.attr('id', 'game-nav-node-'+move.node_id);
                node.data('node_id', move.node_id);

                node.append(this.render_plus_minus(move));
                node.append(this.render_label(move));

                return node;
            },

            render_plus_minus(move) {
                var plus_minus = jQuery('<span/>');
                plus_minus.addClass('game-nav-node-plus-minus');

                if(move.can_collapse) {
                    plus_minus.append('<i class="fa fa-fw fa-plus-square-o"></i>');
                } else {
                    plus_minus.append('<i class="fa fa-fw"></i>');
                }

                return plus_minus;
            },

            render_label(move) {
                var label = jQuery('<span/>');
                label.addClass('game-nav-node-label');

                if(this.active_node.id == move.node_id) {
                    label.addClass('active');
                }

                if(this.color(move.node_id) == 'white') {
                    label.append('<i class="fa fa-fw fa-circle-thin"></i>');
                } else {
                    label.append('<i class="fa fa-fw fa-circle"></i>');
                }

                label.append(move.move);

                return label;
            },

            color(node_id) {
                var node = this.game.board.tree[node_id];
                if(node.action == 'W' || node.action == 'AW') {
                    return 'white';
                }
                return 'black';
            }
        }
    }
</script>