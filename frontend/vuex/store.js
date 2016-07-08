import Vue from 'vue';
import Vuex from 'vuex';
import moment from 'moment';
import { publish_event } from '../events';

Vue.use(Vuex);

export function default_state() {
    return {
        loaded: false,

        route: {},

        auth: {
            user: {
                logged_in: false,
                user_id: "",
                rating: null,
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
        open_games: {},
        active_games: [],
        direct_rooms: {},

        room_has_update: {},
        game_has_update: {},
        
        challenges: []
    };
}

const state = default_state();

export const mutations = {
    MSG_CONNECTION_DATA(state, data) {
        state.auth.user.logged_in = !!data.user_id;
        state.auth.user.user_id = data.user_id;
        state.auth.user.user_display = data.user_display;
        state.auth.user.automatch = data.automatch;
        state.auth.user.wins = data.wins;
        state.auth.user.rating = data.rating;

        Vue.set(state, 'rooms', data.rooms);
        Vue.set(state, 'room_logs', data.room_logs);
        Vue.set(state, 'active_games', data.active_games || []);
        Vue.set(state, 'challenges', data.challenges || []);
        
        (data.open_games || []).forEach(function(game) {
            Vue.set(state.open_games, game.id, game);
        });

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
        
        publish_event('room_message', data);
    },

    MSG_ROOM_LOGS(state, data) {
        Vue.set(state.room_logs, data.room_id, data.logs);
    },

    MSG_ROOM_USER(state, data) {
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
        var game = state.open_games[data.id];

        if(game) {
            game.stage = 'finished';
            game.result = data.result;
        }

        state.active_games = state.active_games.filter(function(game) {
            return game.id != data.id;
        });
    },

    MSG_GAME_DATA(state, data) {
        Vue.set(state.open_games, data.id, data);
        Vue.set(state.game_has_update, data.id, true);
        mutations.UPDATE_GAME_TIME(state, data.id);
    },

    MSG_GAME_UPDATE(state, data) {
        var game = state.open_games[data.game_id];

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
        publish_event('game_update', game);

        mutations.UPDATE_GAME_TIME(state, data.game_id);
    },
    
    MSG_GAME_INFO(state, data) {
        var game = state.open_games[data.game_id];

        if(game) {
            game.title = data.title;
            game.black_display = data.black_display;
            game.white_display = data.white_display;
        }
    },

    MSG_USER_STATUS(state, user) {
        if(user.id == state.auth.user.user_id) {
            state.auth.user.rating = user.rating;
            state.auth.user.wins = user.wins;
        }

        Object.keys(state.room_users).forEach(function(room_id) {
            if(user.is_online) {
                state.room_users[room_id].forEach(function(ru) {
                    if(ru.user_id == user.id) {
                        ru.user_rating = user.rating;
                        return false;
                    }
                });
            } else {
                state.room_users[room_id] = state.room_users[room_id].filter(function(ru) {
                    return ru.user_id != user.id;
                });
            }
        });
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
    
    MSG_DEMO_CURRENT_NODE_ID(state, data) {
        var game = state.open_games[data.game_id];

        if(!game) {
            return;
        }
        
        game.board.current_node_id = data.node_id;
    },
    
    MSG_CHALLENGES(state, data) {
        Vue.set(state, 'challenges', data);
    },
    
    UPDATE_ROUTE(state, route) {
        Vue.set(state, 'route', route);
    },
    
    TOGGLE_SIDEBAR(state) {
        state.sidebar.open = !state.sidebar.open;
    },
    
    UPDATE_GAME_TIME(state, id) {
        var game = state.open_games[id];

        if(!game || !game.timing) {
            return;
        }

        if(game.is_demo || !game.board.tree || (!game.is_demo && game.stage == 'finished') ||
            moment.utc(game.timing.start_at).diff(moment.utc()) > 0) {
            return;
        }

        // TODO: move to separate js and implement other systems
        var node = game.board.tree[game.board.current_node_id];
        var elapsed = Math.abs(moment.utc(game.timing.timing_updated_at).diff(moment.utc())) / 1000;

        if(node && (node.action == 'B' || (node.parent_id === null && node.action == 'E'))) {
            game.timing.white_main -= elapsed;
        } else {
            game.timing.black_main -= elapsed;
        }

        game.timing.timing_updated_at = moment.utc();
    },

    CLOSE_GAME(state, game_id) {
        var game = state.open_games[game_id];

        if(game) {
            Vue.delete(state.room_logs, game.room_id);
            Vue.delete(state.room_has_update, game.room_id);
            Vue.delete(state.open_games, game_id);
        }

        Vue.delete(state.game_has_update, game_id);

        if(state.route.name == "game" && state.route.params.game_id == game_id) {
            state.route.router.go({name: 'active_games'});
        }
    },
    
    ROOM_USERS(state, room_id, users) {
        Vue.set(state.room_users, room_id, users);
    },
    
    CLOSE_DIRECT_ROOM(state, user_id) {
        var room = state.direct_rooms[user_id];
        if(!room) {
            return;
        }

        Vue.delete(state.direct_rooms, user_id);
        Vue.delete(state.room_logs, room.room_id);
        Vue.delete(state.room_has_update, room.room_id);

        if(state.route.name == "user_message" && state.route.params.user_id == user_id) {
            state.route.router.go({name: 'active_games'});
        }
    },
    
    CLEAR_ROOM_UPDATE(state, room_id) {
        Vue.set(state.room_has_update, room_id, false);
    },
    
    CLEAR_GAME_UPDATE(state, game_id) {
        Vue.set(state.game_has_update, game_id, false);
    }
};

export default new Vuex.Store({
    state,
    mutations
});