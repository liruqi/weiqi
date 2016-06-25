<template>
    <div v-el:board class="qi-board"></div>
    <div v-if="confirm_coord != null" class="board-confirm-click text-right">
        <button type="button" @click="confirm_click">Confirm</button>
    </div>
</template>

<script>
    import { construct_pos, coord_to_2d } from '../board';

    export default {
        props: ['board', 'current_node_id', 'current_color', 'coordinates', 'can_click', 'mouse_shadow',
            'allow_shadow_move', 'current', 'highlight_coord'],

        data() {
            return {
                wgo: null,
                resize_interval: null,
                confirm_coord: null,
                click_event: null,
                mouse_coord: null,
                pos: []
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
            'board.tree[current_node_id]': {
                handler: function() {
                    this.draw();
                    this.$dispatch('board-update');
                },
                deep: true
            },

            'coordinates': function(val) {
                this.draw();

                if(val) {
                    this.draw_coordinates();
                }
            },

            'mouse_shadow': function() {
                this.draw_mouse_shadow();
            },

            'current': function() {
                this.draw_mouse_shadow();
            },

            'highlight_coord': function(hi) {
                if(hi) {
                    this.draw_coord_highlighting();
                } else {
                    this.draw();
                }
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

                if(!this.can_click) {
                    return;
                }

                var coord;

                this.confirm_coord = null;
                this.click_event = null;

                if(event.type == 'touchstart') {
                    coord = this.get_mouse_coord(event.touches[0]);
                    if(coord !== null) {
                        this.confirm_coord = coord;
                        this.click_event = event;
                        this.draw();
                    }
                } else {
                    coord = this.get_mouse_coord(event);
                    if(coord !== null) {
                        this.$dispatch('board-click', coord, event, false);
                    }
                }
            },

            confirm_click() {
                this.$dispatch('board-click', this.confirm_coord, this.click_event, true);
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

                if(x < 0 || y < 0 || x >= this.board.size || y >= this.board.size) {
                    return null;
                }

                return x + y*this.board.size;
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

                var pos = construct_pos(this.board, this.current_node_id);
                var node = this.board.tree[this.current_node_id];

                pos.forEach(function(color, coord) {
                    var params = coord_to_2d(coord, this.board.size);

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

                this.pos = pos;
            },

            draw_touch_shadow() {
                if(this.confirm_coord !== null) {
                    var coord = coord_to_2d(this.confirm_coord, this.board.size);
                    var color = (this.current_color == 'o' ? WGo.W : WGo.B);
                    this.wgo.addObject({x: coord.x, y: coord.y, c: color, type: 'outline'});
                }
            },

            draw_symbols() {
                var node = this.board.tree[this.current_node_id];

                if(!node || !node.symbols) {
                    return;
                }

                Object.keys(node.symbols).forEach(function(coord) {
                    var xy = coord_to_2d(+coord, this.board.size);
                    var symbols = ['TR', 'SQ', 'CR'];

                    if(symbols.indexOf(node.symbols[coord]) === -1) {
                        return;
                    }

                    this.wgo.addObject({x: xy.x, y: xy.y, type: node.symbols[coord]})
                }.bind(this));
            },

            draw_labels() {
                var node = this.board.tree[this.current_node_id];

                if(!node || !node.labels) {
                    return;
                }

                Object.keys(node.labels).forEach(function(coord) {
                    var xy = coord_to_2d(+coord, this.board.size);
                    var label = node.labels[coord];
                    this.wgo.addObject({x: xy.x, y: xy.y, type: 'LB', text: label})
                }.bind(this));
            },

            draw_move_marker() {
                var node = this.board.tree[this.current_node_id];

                if(node && (node.action == 'B' || node.action == 'W') && node.move >= 0) {
                    var coord = node.move;
                    var xy = coord_to_2d(coord, this.board.size);

                    this.wgo.addObject({x: xy.x, y: xy.y, type: "CR"})
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
                if(coord == this.mouse_coord || !this.mouse_shadow) {
                    return;
                }

                this.remove_mouse_shadow();
                this.mouse_coord = coord;
                this.draw_mouse_shadow();
            },

            draw_mouse_shadow() {
                this.remove_mouse_shadow();

                if(this.mouse_coord === null || !this.mouse_shadow) {
                    return;
                }

                if(!this.allow_shadow_move && this.pos.length > 0 &&
                        (this.pos[this.mouse_coord] == 'B' || this.pos[this.mouse_coord] == 'W')) {
                    return;
                }

                if(this.mouse_coord !== null) {
                    var xy = coord_to_2d(this.mouse_coord, this.board.size);
                    var color = (this.current == 'o' ? WGo.W : WGo.B);
                    this.wgo.addObject({x: xy.x, y: xy.y, c: color, type: "outline"});
                }
            },

            remove_mouse_shadow() {
                if(this.mouse_coord !== null) {
                    var old_xy = coord_to_2d(this.mouse_coord, this.board.size);
                    this.wgo.removeObject({x: old_xy.x, y: old_xy.y, type: "outline"});
                }
            },

            toggle_coordinates() {
                this.coordinates = !this.coordinates;
                this.draw();
            },

            draw_coord_highlighting() {
                if(this.highlight_coord !== null) {
                    var xy = coord_to_2d(this.highlight_coord, this.board.size);
                    this.wgo.addObject({x: xy.x, y: xy.y, c: 'red', type: 'CR'});
                }
            }
        }
    }
</script>
