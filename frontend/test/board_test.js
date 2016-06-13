import { assert } from 'chai';
import { current_color } from '../board';

describe('current_color', function() {
    it('should handle empty boards', function () {
        var board = {
            tree: []
        };
        
        assert.equal(current_color(board, null), 'x');
    });
    
    it('should return the correct color for alternate play', function () {
        var board = {
            tree: [{action: 'B'}]
        };
        
        assert.equal(current_color(board, board.tree.length-1), 'o');
        
        board.tree.push({action: 'W', parent_id: 0});
        assert.equal(current_color(board, board.tree.length-1), 'x');
        
        board.tree.push({action: 'B', parent_id: 1});
        assert.equal(current_color(board, board.tree.length-1), 'o');
    });
    
    it('should handle handicap games', function() {
        var board = {
            tree: [{action: 'E', parent_id: null}]
        };

        assert.equal(current_color(board, board.tree.length-1), 'o');
    });
});
