export function createGame() {
    return {
        Demo: false,

        Board: {
            current_node_id: 0,
            
            Tree: [{
                parent_id: -1,
                Children: [1, 2]
            }, {
                parent_id: 0,
                Children: []
            }, {
                parent_id: 0,
                Children: []
            }]
        }
    };
}
