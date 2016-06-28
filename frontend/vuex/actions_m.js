import { mutations } from './store';
import * as socket from '../socket';


export function load_room_users(state, room_id) {
    socket.send('rooms/users', {'room_id': room_id}, function (data) {
        mutations.ROOM_USERS(state, room_id, data.users);
    });
}
