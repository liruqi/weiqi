export function createGame() {
    return {
        is_demo: false,

        board: {
            current_node_id: 0,
            
            tree: [{
                parent_id: -1,
                children: [1, 2]
            }, {
                parent_id: 0,
                children: []
            }, {
                parent_id: 0,
                children: []
            }]
        }
    };
}
