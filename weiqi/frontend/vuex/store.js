import Vue from 'vue';
import Vuex from 'vuex';
import moment from 'moment';
import * as socket from '../socket';

Vue.use(Vuex);

const state = {
    loaded: false,
    
    route: {},
    
    auth: {
        user: {
            logged_in: false,
            user_id: "",
            rating: null,
            avatar_url: "",
            automatch: false,
            wins: 0
        }
    },
    
    sidebar: {
        open: true
    },
    
    rooms: [],
    room_logs: {},
    room_users: {},
    open_games: [],
    active_games: [],
    direct_rooms: {},

    room_has_update: {},
    game_has_update: {}
};

const mutations = {
    MSG_CONNECTION_DATA(state, data) {
        state.auth.user.logged_in = !!data.user_id;
        state.auth.user.user_id = data.user_id;
        state.auth.user.user_display = data.user_display;
        state.auth.user.avatar_url = '/api/users/' + data.user_id + '/avatar';
        state.auth.user.automatch = data.automatch;
        state.auth.user.wins = data.wins;
        state.auth.user.rating = data.rating;

        Vue.set(state, 'rooms', data.rooms);
        Vue.set(state, 'room_logs', data.room_logs);
        Vue.set(state, 'open_games', data.open_games || []);
        Vue.set(state, 'active_games', data.active_games || []);

        (data.direct_rooms || []).forEach(function(direct) {
            mutations.MSG_LOAD_DIRECT_ROOM(state, direct);
        });

        state.loaded = true;
    },

    MSG_ROOM_MESSAGE(state, data) {
        if(!state.room_logs[data.room_id]) {
            Vue.set(state.room_logs, data.room_id, []);
        }

        state.room_logs[data.room_id].push(data);

        Vue.set(state.room_has_update, data.room_id, true);
    },

    MSG_ROOM_USER(state, data) {
        if(data.user_id == state.auth.user.user_id) {
            state.auth.user.rating = data.user_rating;
        }

        if(state.direct_rooms[data.user_id]) {
            state.direct_rooms[data.user_id].is_online = true;
        }

        if(!state.room_users[data.room_id]) {
            return;
        }

        state.room_users[data.room_id] = state.room_users[data.room_id].filter(function(user) {
            return user.user_id != data.user_id;
        });
        
        state.room_users[data.room_id].push(data);
    },
    
    MSG_ROOM_USER_LEFT(state, data) {
        if(state.direct_rooms[data.user_id]) {
            state.direct_rooms[data.user_id].is_online = false;
        }

        if(!state.room_users[data.room_id]) {
            return;
        }
        
        state.room_users[data.room_id] = state.room_users[data.room_id].filter(function(user) {
            return user.user_id != data.user_id;
        });
    },

    MSG_AUTOMATCH_STATUS(state, data) {
        state.auth.user.automatch = data.in_queue;
    },
    
    MSG_GAME_STARTED(state, data) {
        var game = state.active_games.find(function(game) {
            return game.id == data.id;
        });
        
        if(game && game.is_demo) {
            game.stage = 'playing';
        } else if(!game) {
            state.active_games.push(data);
        }

        if(!data.is_demo && (data.black_user_id == state.auth.user.user_id || data.white_user_id == state.auth.user.user_id)) {
            state.route.router.go({name: 'game', params: {game_id: data.id}});
        }
    },

    MSG_GAME_FINISHED(state, data) {
        var game = state.open_games.find(function(game) {
            return game.id == data.game_id;
        });

        if(game) {
            game.stage = 'finished';
            game.result = data.result;
        }

        state.active_games = state.active_games.filter(function(game) {
            return game.id != data.game_id;
        });
    },

    MSG_GAME_DATA(state, data) {
        state.open_games = state.open_games.filter(function(game) {
            return game.id != data.id;
        });

        state.open_games.push(data);

        Vue.set(state.game_has_update, data.id, true);

        mutations.UPDATE_GAME_TIME(state, data.id);
    },

    MSG_GAME_UPDATE(state, data) {
        var game = state.open_games.find(function(game) {
            return game.id == data.game_id;
        });

        if(!game) {
            return;
        }

        game.stage = data.stage;
        game.result = data.result;
        game.timing = data.timing;

        if(data.node) {
            if(!game.board.tree) {
                Vue.set(game.board, 'tree', []);
            }

            if (!game.board.tree[data.node.id]) {
                // This value will be needed to detect if a game update created a new node.
                // Useful for determining if a sound should be played.
                Vue.set(game.board, 'last_inserted_node_id', data.node.id);
                game.board.tree.push(data.node);
            } else {
                game.board.tree.$set(data.node.id, data.node);
            }

            game.board.current_node_id = data.node.id;

            if(data.node.parent_id !== null) {
                if (!game.board.tree[data.node.parent_id].children) {
                    Vue.set(game.board.tree[data.node.parent_id], 'children', []);
                }

                if(game.board.tree[data.node.parent_id].children.indexOf(data.node.id) == -1) {
                    game.board.tree[data.node.parent_id].children.push(data.node.id);
                }
            }
        }

        Vue.set(state.game_has_update, data.game_id, true);

        mutations.UPDATE_GAME_TIME(state, data.game_id);
    },
    
    MSG_LOAD_DIRECT_ROOM(state, room) {
        Vue.set(state.direct_rooms, room.other_user_id, {
            room_id: room.room.id,
            other_user_id: room.other_user_id,
            other_display: room.other_display,
            is_online: room.is_online,
            is_active: room.is_active
        });
        
        Vue.set(state.room_logs, room.room.id, room.room_logs);
        Vue.set(state.room_has_update, room.room.id, room.has_unread);
    },
    
    UPDATE_ROUTE(state, route) {
        Vue.set(state, 'route', route);
    },
    
    TOGGLE_SIDEBAR(state) {
        state.sidebar.open = !state.sidebar.open;
    },
    
    UPDATE_GAME_TIME(state, id) {
        var game = state.open_games.find(function(game) {
            return game.id == id;
        });

        if(!game.timing) {
            return;
        }

        if(!game || game.is_demo || !game.board.tree || (!game.is_demo && game.stage == 'finished') ||
            moment(game.timing.start_at).diff(moment.utc()) > 0) {
            return;
        }

        var node = game.board.tree[game.board.current_node_id];
        var current = 'B';
        var timing = game.timing.black;

        if(node && (node.action == 'B' || (!node.parent_id >= 0 && node.action == 'E'))) {
            current = 'W';
            timing = game.timing.white;
        }

        timing.Main -= Math.abs(moment(game.timing.LastUpdateAt).diff(moment.utc())) * 1000000;
        game.timing.LastUpdateAt = moment.utc();
    },

    OPEN_GAME(state, game_id) {
        var game = state.open_games.find(function(game) {
            return game.id == game_id;
        });

        if(game && game.board) {
            return;
        }

        socket.send('games/open', {'game_id': game_id});
    },

    CLOSE_GAME(state, game_id) {
        socket.send('games/close', {'game_id': game_id});

        state.open_games = state.open_games.filter(function(game) {
            return game.id != game_id;
        });
    },
    
    LOAD_ROOM_USERS(state, room_id) {
        if(!room_id || !!state.room_users[room_id]) {
            return;
        }

        socket.send('rooms/users', {'room_id': room_id}, function(data) {
            Vue.set(state.room_users, room_id, data.users);
        });
    },
    
    RELOAD_USER_AVATAR(state) {
        state.auth.user.avatar_url = '/api/users/' + state.auth.user.user_id + '/avatar?' + (new Date()).getTime();
    },
    
    LOAD_DIRECT_ROOM(state, user_id) {
        socket.send('rooms/open_direct', {'user_id': user_id}, function(data) {
            mutations.MSG_LOAD_DIRECT_ROOM(state, data);
        });
    },
    
    MSG_DIRECT_MESSAGE(state, data) {
        if(data.user_id == state.auth.user.user_id || state.direct_rooms[data.user_id]) {
            mutations.MSG_ROOM_MESSAGE(state, data);
        } else {
            mutations.LOAD_DIRECT_ROOM(state, data.user_id);
        }
    },
    
    CLEAR_ROOM_UPDATE(state, room_id) {
        Vue.set(state.room_has_update, room_id, false);

        var is_direct = Object.keys(state.direct_rooms).find(function(user_id) {
            return state.direct_rooms[user_id].room_id == room_id;
        });

        if(is_direct) {
            socket.send('rooms/mark_read', {'room_id': room_id});
        }
    },
    
    CLEAR_GAME_UPDATE(state, game_id) {
        Vue.set(state.game_has_update, game_id, false);
    }
};

export default new Vuex.Store({
    state,
    mutations
});