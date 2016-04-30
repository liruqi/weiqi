export function createGame() {
    return {
        Demo: false,

        Board: {
            CurrentNodeID: 0,
            
            Tree: [{
                ParentID: -1,
                Children: [1, 2]
            }, {
                ParentID: 0,
                Children: []
            }, {
                ParentID: 0,
                Children: []
            }]
        }
    };
}
