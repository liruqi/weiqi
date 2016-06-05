<template>
    <div v-el:board class="qi-board"></div>
    <div v-if="confirm_coord != null" class="board-confirm-click text-right">
        <button type="button" @click="confirm_click">Confirm</button>
    </div>
</template>

<script>
    export default {
        props: ['board', 'current_node_id', 'coordinates', 'mouse_shadow', 'current'],

        data() {
            return {
                wgo: null,
                resize_interval: null,
                confirm_coord: null,
                click_event: null,
                mouse_coord: null
            }
        },

        ready() {
            this.wgo = new WGo.Board(this.$els.board, {
                width:      500,
                background: "/static/images/board/board.jpg",
                size:       this.board.size
            });

            this.set_size();
            this.draw_coordinates();
            this.draw();

            this.wgo.addEventListener("touchstart", this.click_handler);
            this.wgo.addEventListener("click", this.click_handler);
            this.wgo.addEventListener("mousemove", this.mousemove_handler);
            jQuery(this.$els.board).on('DOMMouseScroll mousewheel', this.scroll_handler);


            var el = jQuery(this.$els.board).parent();
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
            clearInterval(this.resize_interval);
        },

        watch: {
            'current_node_hash': function() {
                this.draw();
                this.$dispatch('board-update');
            },

            'coordinates': function() {
                this.draw();
            },

            'mouse_shadow': function() {
                this.draw();
            }
        },

        computed: {
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
                var parent_height = jQuery(this.$els.board).parent().height();
                var siblings_height = 0;

                jQuery(this.$els.board).siblings().each(function() {
                    siblings_height += jQuery(this).height();
                });

                var height = parent_height - siblings_height;
                var width = jQuery(this.$els.board).width();
                var min = Math.min(height, width);

                if(this.wgo.width != min) {
                    this.wgo.setWidth(min);
                }
            },

            mousemove_handler(x, y, event) {
                var coord = this.get_mouse_coord(event);
                this.update_mouse_shadow(coord);
            },

            click_handler(x, y, event) {
                // Stopping the event is required because we are listening to both touchstart and click.
                event.stopPropagation();
                event.preventDefault();

                var coord;

                this.confirm_coord = null;
                this.click_event = null;

                if(event.type == 'touchstart') {
                    coord = this.get_mouse_coord(event.touches[0]);
                    this.confirm_coord = coord;
                    this.click_event = event;
                    this.draw();
                } else {
                    coord = this.get_mouse_coord(event);
                    this.$dispatch('board-click', coord, event);
                }
            },

            confirm_click() {
                this.$dispatch('board-click', this.confirm_coord, this.click_event);
                this.confirm_coord = null;
                this.click_event = null;
            },

            // The WGo implementation of this function does not handle touch events correctly.
            get_mouse_coord(e) {
                var x, y;
                var offset = jQuery(this.$els.board).find('.wgo-board').offset();

                x = (e.clientX - offset.left) * this.wgo.pixelRatio;
                x -= this.wgo.left;
                x /= this.wgo.fieldWidth;
                x = Math.round(x);

                y = (e.clientY - offset.top) * this.wgo.pixelRatio;
                y -= this.wgo.top;
                y /= this.wgo.fieldHeight;
                y = Math.round(y);

                var mouse = {
                    x: x >= this.wgo.size ? -1 : x,
                    y: y >= this.wgo.size ? -1 : y
                };

                return mouse.x + mouse.y*this.board.size;
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

                this.draw_touch_shadow();

                this.draw_symbols();
                this.draw_labels();
                this.draw_move_marker();
            },

            draw_touch_shadow() {
                if(this.confirm_coord !== null) {
                    console.log(this.confirm_coord);
                    var xy = this.coord_to_2d(this.confirm_coord);
                    this.wgo.addObject({x: xy[0], y: xy[1], c: WGo.B, type: 'outline'});
                }
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

            update_mouse_shadow(coord) {
                if(coord == this.mouse_coord || coord < 0) {
                    return;
                }

                if(this.mouse_coord !== null) {
                    var old_xy = this.coord_to_2d(this.mouse_coord);
                    this.wgo.removeObject({x: old_xy[0], y: old_xy[1], type: "outline"});
                }

                if(this.mouse_shadow) {
                    var xy = this.coord_to_2d(coord);
                    var color = (this.current == 'o' ? WGo.W : WGo.B);
                    this.wgo.addObject({x: xy[0], y: xy[1], c: color, type: "outline"});

                    this.mouse_coord = coord;
                }
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
                        if(node.edits) {
                            Object.keys(node.edits).forEach(function (key) {
                                pos[+key] = colors[node.edits[key]];
                            });
                        }
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
            },
        }
    }
</script>