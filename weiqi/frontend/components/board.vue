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
                resizeInterval: null
            }
        },

        ready() {
            this.wgo = new WGo.Board(this.$el, {
                width:      500,
                background: "/assets/images/board/board.jpg",
                size:       this.board.Size
            });

            this.setSize();
            this.drawCoordinates();
            this.draw();

            this.wgo.addEventListener("click", this.clickHandler);
            jQuery(this.$el).on('DOMMouseScroll mousewheel', this.scrollHandler);


            var el = jQuery(this.$el).parent();
            var lastWidth = el.width();
            var lastHeight = el.height();

            this.resizeInterval = setInterval(function() {
                var width = el.width();
                var height= el.height();

                if(width != lastWidth || height != lastHeight) {
                    this.setSize();
                    lastWidth = width;
                    lastHeight = height;
                }
            }.bind(this), 1000/60);
        },

        destroyed() {
            this.wgo.removeEventListener("click", this.clickHandler);
            jQuery(this.$el).off('mousewheel');
            jQuery(this.$el).off('DOMMouseScroll');

            clearInterval(this.resizeInterval);
        },

        watch: {
            'currentNodeHash': function() {
                this.draw();
                this.$dispatch('board-update');
            }
        },

        computed: {
            currentNodeID() {
                if(this.force_node_id !== false) {
                    return this.force_node_id;
                }
                return this.board.CurrentNodeID;
            },

            currentNodeHash() {
                if((this.board.Tree || []).length < 1) {
                    return null;
                }

                var node = this.board.Tree[this.currentNodeID];
                return JSON.stringify(node);
            }
        },

        methods: {
            setSize() {
                var parentHeight = jQuery(this.$el).parent().height();
                var siblingsHeight = 0;

                jQuery(this.$el).siblings().each(function() {
                    siblingsHeight += jQuery(this).height();
                });

                var height = parentHeight - siblingsHeight;
                var width = jQuery(this.$el).width();
                var min = Math.min(height, width);

                if(this.wgo.width != min) {
                    this.wgo.setWidth(min);
                }
            },

            clickHandler(x, y) {
                var coord = x + y*this.board.Size;
                this.$dispatch('board-click', coord);
            },

            scrollHandler(e) {
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

                if((this.board.Tree || []).length < 1) {
                    return;
                }

                var pos = this.constructPos();
                var node = this.board.Tree[this.currentNodeID];

                pos.forEach(function(color, coord) {
                    var y = Math.floor(coord/this.board.Size);
                    var x = coord - y*this.board.Size;
                    var params = {x: x, y: y};

                    if(color == 'B') {
                        params.c = WGo.B;
                    } else if(color == 'W') {
                        params.c = WGo.W;
                    }

                    if(node && node.ScorePoints) {
                        if(node.MarkedDead && node.MarkedDead[coord]) {
                            params.type = "outline"
                        }

                        if(color == '.' && node.ScorePoints[coord] == 1) {
                            params.type = "mini";
                            params.c = WGo.B;
                        } else if(color == '.' && node.ScorePoints[coord] == 2) {
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

                this.drawMoveMarker();
            },

            drawMoveMarker() {
                var node = this.board.Tree[this.currentNodeID];

                if(node && (node.Action == 'B' || node.Action == 'W') && node.Move >= 0) {
                    var coord = node.Move;
                    var y = Math.floor(coord/this.board.Size);
                    var x = coord - y*this.board.Size;

                    this.wgo.addObject({x: x, "y": y, "type": "CR"})
                }
            },

            drawCoordinates() {
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

            constructPos() {
                var pos = this.emptyPos(this.board.Size);
                var nodes = this.currentNodePath();

                nodes.forEach(function(node) { this.applyNode(pos, node) }.bind(this));

                return pos;
            },

            emptyPos(size) {
                var pos = [];

                for(var i=0; i<size*size; i++) {
                    pos.push('.');
                }

                return pos;
            },

            currentNodePath() {
                if((this.board.Tree || []).length < 1) {
                    return [];
                }

                var nodes = [];
                var curNode = this.board.Tree[this.currentNodeID];

                while(curNode) {
                    nodes.unshift(curNode);
                    curNode = this.board.Tree[curNode.ParentID];
                }

                return nodes;
            },

            applyNode(pos, node) {
                var colors = {0: 'W', 1: 'B'};

                switch(node.Action) {
                    case 'B':
                    case 'W':
                        if(node.Move >= 0) {
                            pos[node.Move] = node.Action;
                        }
                        break;

                    case 'E':
                        Object.keys(node.Edits).forEach(function(key) {
                            pos[+key] = colors[node.Edits[key]];
                        });
                        break;
                }

                if(node.Captures) {
                    node.Captures.forEach(function (coord) {
                        pos[coord] = '.';
                    });
                }
            },

            toggleCoordinates() {
                this.coordinates = !this.coordinates;
                this.draw();
            }
        }
    }
</script>