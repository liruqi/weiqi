import { current_color } from './board';

export function is_current_player(game, node_id, user_id) {
    var current = current_color(game.board, node_id);
    return (current == 'x' && game.black_user_id == user_id) || (current == 'o' && game.white_user_id == user_id);
}