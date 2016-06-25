import { assert } from 'chai';
import { current_color, coord_to_str, parse_coord, is_valid_coord } from '../board';

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

describe('coord_to_str', function() {
    it('should convert coordinates to strings', function() {
        assert.equal(coord_to_str(0, 9), 'A9');
        assert.equal(coord_to_str(8, 9), 'J9');
        assert.equal(coord_to_str(72, 9), 'A1');
        assert.equal(coord_to_str(80, 9), 'J1');
    });
});

describe('parse_coord', function() {
    it('should parse coordinates', function() {
        assert.equal(parse_coord('a9', 9), 0);
        assert.equal(parse_coord('h9', 9), 7);
        assert.equal(parse_coord('j9', 9), 8);
        assert.equal(parse_coord('a1', 9), 72);
        assert.equal(parse_coord('j1', 9), 80);
    });
});

describe('is_valid_coord', function() {
    it('should respect board sizes', function() {
        assert.isTrue(is_valid_coord('a1', 9));
        assert.isTrue(is_valid_coord('j1', 9));
        assert.isTrue(is_valid_coord('a9', 9));
        assert.isTrue(is_valid_coord('j9', 9));
        
        assert.isFalse(is_valid_coord('i1', 9));
        assert.isFalse(is_valid_coord('k1', 9));
    });
});