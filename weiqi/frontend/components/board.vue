<template>
    <div class="qi-board"></div>
</template>

<script>
    export default {
        props: {
            board: {
                type: Object,
                required: true
            },

            force_node_id: false,

            coordinates: {
                type: Boolean,
                default: true
            }
        },

        data() {
            return {
                wgo: null,
                resize_interval: null
            }
        },

        ready() {
            this.wgo = new WGo.Board(this.$el, {
                width:      500,
                background: "/static/images/board/board.jpg",
                size:       this.board.size
            });

            this.set_size();
            this.draw_coordinates();
            this.draw();

            this.wgo.addEventListener("click", this.click_handler);
            jQuery(this.$el).on('DOMMouseScroll mousewheel', this.scroll_handler);


            var el = jQuery(this.$el).parent();
            var last_width = el.width();
            var last_height = el.height();

            this.resize_interval = setInterval(function() {
                var width = el.width();
                var height= el.height();

                if(width != last_width || height != last_height) {
                    this.set_size();
                    last_width = width;
                    last_height = height;
                }
            }.bind(this), 1000/60);
        },

        destroyed() {
            this.wgo.removeEventListener("click", this.click_handler);
            jQuery(this.$el).off('mousewheel');
            jQuery(this.$el).off('DOMMouseScroll');

            clearInterval(this.resize_interval);
        },

        watch: {
            'current_node_hash': function() {
                this.draw();
                this.$dispatch('board-update');
            }
        },

        computed: {
            current_node_id() {
                if(this.force_node_id !== false) {
                    return this.force_node_id;
                }
                return this.board.current_node_id;
            },

            current_node_hash() {
                if((this.board.tree || []).length < 1) {
                    return null;
                }

                var node = this.board.tree[this.current_node_id];
                return JSON.stringify(node);
            }
        },

        methods: {
            set_size() {
                var parent_height = jQuery(this.$el).parent().height();
                var siblings_height = 0;

                jQuery(this.$el).siblings().each(function() {
                    siblings_height += jQuery(this).height();
                });

                var height = parent_height - siblings_height;
                var width = jQuery(this.$el).width();
                var min = Math.min(height, width);

                if(this.wgo.width != min) {
                    this.wgo.setWidth(min);
                }
            },

            click_handler(x, y, event) {
                var coord = x + y*this.board.size;
                this.$dispatch('board-click', coord, event);
            },

            scroll_handler(e) {
                e.preventDefault();

                var scroll = 1;
                var wheel = e.originalEvent;

                if(wheel.wheelDelta > 0 || wheel.detail < 0) {
                    scroll = -1;
                }

                this.$dispatch('board-scroll', scroll);
            },

            draw() {
                this.wgo.removeAllObjects();

                if((this.board.tree || []).length < 1) {
                    return;
                }

                var pos = this.construct_pos();
                var node = this.board.tree[this.current_node_id];

                pos.forEach(function(color, coord) {
                    var xy = this.coord_to_2d(coord);
                    var params = {x: xy[0], y: xy[1]};

                    if(color == 'B') {
                        params.c = WGo.B;
                    } else if(color == 'W') {
                        params.c = WGo.W;
                    }

                    if(node && node.score_points) {
                        if(node.marked_dead && node.marked_dead[coord]) {
                            params.type = "outline"
                        }

                        if(color == '.' && node.score_points[coord] == 'x') {
                            params.type = "mini";
                            params.c = WGo.B;
                        } else if(color == '.' && node.score_points[coord] == 'o') {
                            params.type = "mini";
                            params.c = WGo.W;
                        } else if(color == '.') {
                            return;
                        }
                    } else if(color == '.') {
                        return;
                    }

                    this.wgo.addObject(params);
                }.bind(this));

                this.draw_symbols();
                this.draw_labels();
                this.draw_move_marker();
            },

            draw_symbols() {
                var node = this.board.tree[this.current_node_id];

                if(!node || !node.symbols) {
                    return;
                }

                Object.keys(node.symbols).forEach(function(coord) {
                    var xy = this.coord_to_2d(+coord);
                    var symbols = ['TR', 'SQ', 'CR'];

                    if(symbols.indexOf(node.symbols[coord]) === -1) {
                        return;
                    }

                    this.wgo.addObject({x: xy[0], y: xy[1], type: node.symbols[coord]})
                }.bind(this));
            },

            draw_labels() {
                var node = this.board.tree[this.current_node_id];

                if(!node || !node.labels) {
                    return;
                }

                Object.keys(node.labels).forEach(function(coord) {
                    var xy = this.coord_to_2d(+coord);
                    var label = node.labels[coord];
                    this.wgo.addObject({x: xy[0], y: xy[1], type: 'LB', text: label})
                }.bind(this));
            },

            draw_move_marker() {
                var node = this.board.tree[this.current_node_id];

                if(node && (node.action == 'B' || node.action == 'W') && node.move >= 0) {
                    var coord = node.move;
                    var xy = this.coord_to_2d(coord);

                    this.wgo.addObject({x: xy[0], y: xy[1], type: "CR"})
                }
            },

            draw_coordinates() {
                if(!this.coordinates) {
                    this.wgo.setSection({top: 0, right: 0, bottom: 0, left: 0});
                    return;
                }

                this.wgo.setSection({
                    top: -0.5,
                    left: -0.5,
                    right: -0.5,
                    bottom: -0.5
                });

                var coordinates = {
                    // draw on grid layer
                    grid: {
                        draw: function(args, board) {
                            var ch, t, xright, xleft, ytop, ybottom;

                            this.fillStyle = "rgba(0,0,0,0.7)";
                            this.textBaseline="middle";
                            this.textAlign="center";
                            this.font = board.stoneRadius+"px "+(board.font || "");

                            xright = board.getX(-0.75);
                            xleft = board.getX(board.size-0.25);
                            ytop = board.getY(-0.75);
                            ybottom = board.getY(board.size-0.25);

                            for(var i = 0; i < board.size; i++) {
                                ch = i+"A".charCodeAt(0);
                                if(ch >= "I".charCodeAt(0)) ch++;

                                t = board.getY(i);
                                this.fillText(board.size-i, xright, t);
                                this.fillText(board.size-i, xleft, t);

                                t = board.getX(i);
                                this.fillText(String.fromCharCode(ch), t, ytop);
                                this.fillText(String.fromCharCode(ch), t, ybottom);
                            }

                            this.fillStyle = "black";
                        }
                    }
                };

                this.wgo.addCustomObject(coordinates);
            },

            construct_pos() {
                var pos = this.empty_pos(this.board.size);
                var nodes = this.current_node_path();

                nodes.forEach(function(node) { this.apply_node(pos, node) }.bind(this));

                return pos;
            },

            empty_pos(size) {
                var pos = [];

                for(var i=0; i<size*size; i++) {
                    pos.push('.');
                }

                return pos;
            },

            current_node_path() {
                if((this.board.tree || []).length < 1) {
                    return [];
                }

                var nodes = [];
                var cur_node = this.board.tree[this.current_node_id];

                while(cur_node) {
                    nodes.unshift(cur_node);
                    cur_node = this.board.tree[cur_node.parent_id];
                }

                return nodes;
            },

            apply_node(pos, node) {
                var colors = {'x': 'B', 'o': 'W', '.': '.'};

                switch(node.action) {
                    case 'B':
                    case 'W':
                        if(node.move >= 0) {
                            pos[node.move] = node.action;
                        }
                        break;

                    case 'E':
                        Object.keys(node.edits).forEach(function(key) {
                            pos[+key] = colors[node.edits[key]];
                        });
                        break;
                }

                if(node.captures) {
                    node.captures.forEach(function (coord) {
                        pos[coord] = '.';
                    });
                }
            },

            coord_to_2d(coord) {
                var y = Math.floor(coord/this.board.size);
                var x = coord - y*this.board.size;
                return [x, y];
            },

            toggle_coordinates() {
                this.coordinates = !this.coordinates;
                this.draw();
            }
        }
    }
</script>