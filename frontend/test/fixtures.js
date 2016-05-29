export function create_game() {
    return {
        is_demo: false,

        board: {
            current_node_id: 0,
            
            tree: [{
                id: 0,
                parent_id: null,
                children: [1, 2]
            }, {
                id: 1,
                parent_id: 0,
                children: []
            }, {
                id: 2,
                parent_id: 0,
                children: []
            }]
        }
    };
}
