export const serverMessages = {
    "connection_data": makeAction('MSG_CONNECTION_DATA'),
    "room_message": makeAction('MSG_ROOM_MESSAGE'),
    "room_user": makeAction('MSG_ROOM_USER'),
    "room_user_left": makeAction('MSG_ROOM_USER_LEFT'),
    "automatch_status": makeAction('MSG_AUTOMATCH_STATUS'),
    "game_started": makeAction('MSG_GAME_STARTED'),
    "game_finished": makeAction('MSG_GAME_FINISHED'),
    "game_data": makeAction('MSG_GAME_DATA'),
    "game_update": makeAction('MSG_GAME_UPDATE'),
    "load_direct_room": makeAction('MSG_LOAD_DIRECT_ROOM')
};

export const updateRoute = makeAction('UPDATE_ROUTE');
export const toggleSidebar = makeAction('TOGGLE_SIDEBAR');
export const update_game_time = makeAction('UPDATE_GAME_TIME');
export const open_game = makeAction('OPEN_GAME');
export const closeGame = makeAction('CLOSE_GAME');
export const load_room_users = makeAction('LOAD_ROOM_USERS');
export const reloadUserAvatar = makeAction('RELOAD_USER_AVATAR');
export const loadDirectRoom = makeAction('LOAD_DIRECT_ROOM');
export const clear_room_update = makeAction('CLEAR_ROOM_UPDATE');
export const clear_game_update = makeAction('CLEAR_GAME_UPDATE');

function makeAction(type) {
    return ({dispatch}, ...args) => dispatch(type, ...args);
}