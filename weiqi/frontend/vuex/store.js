import Vue from 'vue';
import Vuex from 'vuex';
import moment from 'moment';

Vue.use(Vuex);

const state = {
    loaded: false,
    pong: 0,
    
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
    
    MSG_PONG(state, data) {
        state.pong = data;
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
            state.auth.user.rating = data.Rating;
        }

        if(state.direct_rooms[data.user_id]) {
            state.direct_rooms[data.user_id].IsOnline = data.IsOnline;
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
        if(!state.room_users[data.room_id]) {
            return;
        }
        
        state.room_users[data.room_id] = state.room_users[data.room_id].filter(function(user) {
            return user.user_id != data.user_id;
        });
    },

    MSG_AUTOMATCH_STATUS(state, data) {
        state.auth.user.automatch = data.InQueue;
    },
    
    MSG_GAME_STARTED(state, data) {
        var game = state.active_games.find(function(game) {
            return game.id == data.id;
        });
        
        if(game && game.Demo) {
            game.stage = 'playing';
        } else if(!game) {
            state.active_games.push(data);
        }

        if(!data.Demo && (data.MatchBlack == state.auth.user.user_id || data.MatchWhite == state.auth.user.user_id)) {
            state.route.router.go({name: 'game', params: {game_id: data.id}});
        }
    },

    MSG_GAME_FINISHED(state, data) {
        var game = state.open_games.find(function(game) {
            return game.id == data.game_id;
        });

        if(game) {
            game.stage = 'finished';
            game.Result = data.Result;
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

        game.stage = data.Stage;
        game.Result = data.Result;
        game.Timing = data.Timing;

        if(data.Node) {
            if(!game.Board.Tree) {
                Vue.set(game.Board, 'Tree', []);
            }

            if (!game.Board.Tree[data.Node.id]) {
                // This value will be needed to detect if a game update created a new node.
                // Useful for determining if a sound should be played.
                Vue.set(game.Board, 'LastInsertedNodeID', data.Node.id);
                game.Board.Tree.push(data.Node);
            } else {
                game.Board.Tree.$set(data.Node.id, data.Node);
            }

            game.Board.CurrentNodeID = data.Node.id;

            if(data.Node.ParentID >= 0) {
                if (!game.Board.Tree[data.Node.ParentID].Children) {
                    Vue.set(game.Board.Tree[data.Node.ParentID], 'Children', []);
                }

                if(game.Board.Tree[data.Node.ParentID].Children.indexOf(data.Node.id) == -1) {
                    game.Board.Tree[data.Node.ParentID].Children.push(data.Node.id);
                }
            }
        }

        Vue.set(state.game_has_update, data.game_id, true);

        mutations.UPDATE_GAME_TIME(state, data.game_id);
    },
    
    MSG_LOAD_DIRECT_ROOM(state, room) {
        Vue.set(state.direct_rooms, room.Otheruser_id, {
            room_id: room.Room.id,
            Otheruser_id: room.Otheruser_id,
            IsOnline: room.IsOnline,
            IsActive: room.IsActive
        });
        
        Vue.set(state.room_logs, room.Room.id, room.room_logs);
        Vue.set(state.room_has_update, room.Room.id, room.HasUnread);
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

        if(!game || game.Demo || !game.Board.Tree || (!game.Demo && game.stage == 'finished') ||
            moment(game.Timing.StartAt).diff(moment.utc()) > 0) {
            return;
        }

        var node = game.Board.Tree[game.Board.CurrentNodeID];
        var current = 'B';
        var timing = game.Timing.Black;

        if(node && (node.Action == 'B' || (!node.ParentID >= 0 && node.Action == 'E'))) {
            current = 'W';
            timing = game.Timing.White;
        }

        timing.Main -= Math.abs(moment(game.Timing.LastUpdateAt).diff(moment.utc())) * 1000000;
        game.Timing.LastUpdateAt = moment.utc();
    },

    OPEN_GAME(state, game_id) {
        var game = state.open_games.find(function(game) {
            return game.id == game_id;
        });

        if(game && game.Board) {
            return;
        }

        Vue.http.post('/api/games/'+game_id+'/open');
    },

    CLOSE_GAME(state, game_id) {
        Vue.http.post('/api/games/'+game_id+'/close');

        state.open_games = state.open_games.filter(function(game) {
            return game.id != game_id;
        });
    },
    
    LOAD_ROOM_USERS(state, room_id) {
        if(!room_id || !!state.room_users[room_id]) {
            return;
        }

        Vue.http.get('/api/rooms/'+room_id+'/users').then(function(res) {
            Vue.set(state.room_users, room_id, res.data.users);
        });
    },
    
    RELOAD_USER_AVATAR(state) {
        state.auth.user.avatar_url = '/api/users/' + state.auth.user.user_id + '/avatar?' + (new Date()).getTime();
    },
    
    LOAD_DIRECT_ROOM(state, user_id) {
        Vue.http.post('/api/users/' + user_id + '/open-direct').then(function(res) {
            mutations.MSG_LOAD_DIRECT_ROOM(state, res.data);
        }, function() {})
    },
    
    CLEAR_ROOM_UPDATE(state, room_id) {
        Vue.set(state.room_has_update, room_id, false);

        var isDirect = Object.keys(state.direct_rooms).find(function(user_id) {
            return state.direct_rooms[user_id].room_id == room_id;
        });

        if(isDirect) {
            Vue.http.post('/api/rooms/' + room_id + '/mark-read');
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