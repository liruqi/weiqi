export const serverMessages = {
    "connection_data": makeAction('MSG_CONNECTION_DATA'),
    "RoomMessage": makeAction('MSG_ROOM_MESSAGE'),
    "RoomUser": makeAction('MSG_ROOM_USER'),
    "RoomUserLeft": makeAction('MSG_ROOM_USER_LEFT'),
    "AutomatchStatus": makeAction('MSG_AUTOMATCH_STATUS'),
    "GameStarted": makeAction('MSG_GAME_STARTED'),
    "GameFinished": makeAction('MSG_GAME_FINISHED'),
    "GameData": makeAction('MSG_GAME_DATA'),
    "GameUpdate": makeAction('MSG_GAME_UPDATE'),
    "LoadDirectRoom": makeAction('MSG_LOAD_DIRECT_ROOM')
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