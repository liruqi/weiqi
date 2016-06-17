import { assert } from 'chai';
import { is_current_player } from '../game';

describe('is_current_player', function() {
    it('should return the correct value', function () {
        var game = {
            black_user_id: 1,
            white_user_id: 2,
            board: {
                tree: []
            }
        };
        
        assert.isTrue(is_current_player(game, null, 1));
        assert.isFalse(is_current_player(game, null, 2));
        
        game.board.tree.push({action: 'B'});
        
        assert.isFalse(is_current_player(game, 0, 1));
        assert.isTrue(is_current_player(game, 0, 2));
        
        game.board.tree.push({action: 'W'});
        
        assert.isTrue(is_current_player(game, 1, 1));
        assert.isFalse(is_current_player(game, 1, 2));
    });
});
