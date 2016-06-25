export function current_color(board, node_id) {
    if (board.tree.length == 0) {
        return 'x';
    }

    var node = board.tree[node_id];

    while (node) {
        if (node.action == 'B') {
            return 'o';
        } else if (node.action == 'W') {
            return 'x';
        }

        if (node.parent_id === null) {
            // Handicap game
            return 'o';
        }

        node = board.tree[node.parent_id];
    }
}

export function mainline(board) {
    var main = [];
    var node = board.tree[0];

    while(node) {
        main.push(node.id);

        if(node.children.length > 0) {
            node = board.tree[node.children[0]];
        } else {
            break;
        }
    }

    return main;
}

export function generate_move_tree(board) {
    if(!board.tree || board.tree.length == 0) {
        return [];
    }

    var tree = [];
    var node = board.tree[0];

    add_moves_to_tree(board, tree, node);

    return tree;
}

function add_moves_to_tree(board, tree, node, level, move) {
    level = level || 0;
    move = move || 1;
    var can_collapse = can_collapse_node(board, node.id, level);
    var is_main = (level == 0);

    tree.push({type: 'node', node_id: node.id, can_collapse: can_collapse, move: move});
    move += 1;

    if(can_collapse) {
        var vars = [];

        node.children.forEach(function(child, idx) {
            if(is_main && idx == 0) {
                return;
            }

            var subtree = [];
            add_moves_to_tree(board, subtree, board.tree[child], level+1, move);
            vars.push(subtree);
        });

        tree.push({type: 'variations', vars: vars, parent_id: node.id, move: move});

        if(is_main) {
            add_moves_to_tree(board, tree, board.tree[node.children[0]], level, move);
        }
    } else if(node.children.length == 1) {
        add_moves_to_tree(board, tree, board.tree[node.children[0]], level, move);
    }
}

export function is_single_node(board, node_id) {
    var node = board.tree[node_id];

    if(node.parent_id === null) {
        return true;
    }

    return (board.tree[node.parent_id].children.length - 1) < 1;
}

export function can_collapse_node(board, node_id, level) {
    var node = board.tree[node_id];

    if(level == 0) {
        return node.children.length > 1;
    } else {
        return node.children.length > 1 || (!is_single_node(board, node_id) && node.children.length >= 1);
    }
}

export function construct_pos(board, node_id) {
    var pos = empty_pos(board.size);
    var nodes = node_path(board, node_id);

    nodes.forEach(function(node) {
        apply_node(pos, node)
    });

    return pos;
}

function empty_pos(size) {
    var pos = [];

    for(var i=0; i<size*size; i++) {
        pos.push('.');
    }

    return pos;
}

export function node_path(board, node_id) {
    if((board.tree || []).length < 1) {
        return [];
    }

    var nodes = [];
    var cur_node = board.tree[node_id];

    while(cur_node) {
        nodes.unshift(cur_node);
        cur_node = board.tree[cur_node.parent_id];
    }

    return nodes;
}

function apply_node(pos, node) {
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
}

export function coord_to_2d(coord, size) {
    var y = Math.floor(coord/size);
    var x = coord - y*size;
    return {x: x, y: y};
}

export function coord_to_str(coord, size) {
    var xy = coord_to_2d(coord, size);
    var x = xy.x;
    var y = size - xy.y;
    
    if(x >= 8) {
        x += 1;
    }
    
    return String.fromCharCode('A'.charCodeAt(0) + x) + y;
}

export function parse_coord(coord, size) {
    var x = coord[0].toLowerCase().charCodeAt(0) - 'a'.charCodeAt(0);
    var y = size - parseInt(coord.slice(1));
    
    // There is no 'i' on the board.
    if(coord[0] == 'i') {
        return null;
    }
    
    if(x >= 8) {
        x -= 1;
    }
    
    if(x < 0 || x >= size || y < 0 || y >= size) {
        return null;
    }
    
    return x + y*size;
}

export function is_valid_coord(coord, size) {
    return parse_coord(coord, size) !== null;
}