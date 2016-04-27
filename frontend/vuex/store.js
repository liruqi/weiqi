import Vue from 'vue';
import Vuex from 'vuex';
import * as actions from './actions';
import moment from 'moment';

Vue.use(Vuex);

const state = {
    loaded: false,
    
    route: {},
    
    auth: {
        user: {
            loggedIn: false,
            userID: "",
            rating: null,
            avatarURL: "",
            automatch: false,
            wins: 0
        }
    },
    
    sidebar: {
        open: true
    },
    
    rooms: [],
    roomLogs: {},
    roomUsers: {},
    openGames: [],
    activeGames: [],
    directRooms: {},

    roomHasUpdate: {},
    gameHasUpdate: {}
};

const mutations = {
    MSG_CONNECTION_DATA(state, data) {
        state.auth.user.loggedIn = !!data.UserID;
        state.auth.user.userID = data.UserID;
        state.auth.user.avatarURL = '/api/users/' + data.UserID + '/avatar';
        state.auth.user.automatch = data.Automatch;
        state.auth.user.wins = data.Wins;
        state.auth.user.rating = data.Rating;

        Vue.set(state, 'rooms', data.Rooms);
        Vue.set(state, 'roomLogs', data.RoomLogs);
        Vue.set(state, 'openGames', data.OpenGames || []);
        Vue.set(state, 'activeGames', data.ActiveGames || []);

        (data.DirectRooms || []).forEach(function(direct) {
            mutations.MSG_LOAD_DIRECT_ROOM(state, direct);
        });

        state.loaded = true;
    },

    MSG_ROOM_MESSAGE(state, data) {
        if(!state.roomLogs[data.RoomID]) {
            Vue.set(state.roomLogs, data.RoomID, []);
        }

        state.roomLogs[data.RoomID].push(data);

        Vue.set(state.roomHasUpdate, data.RoomID, true);
    },

    MSG_ROOM_USER(state, data) {
        if(data.UserID == state.auth.user.userID) {
            state.auth.user.rating = data.Rating;
        }

        if(state.directRooms[data.UserID]) {
            state.directRooms[data.UserID].IsOnline = data.IsOnline;
        }

        if(!state.roomUsers[data.RoomID]) {
            return;
        }

        state.roomUsers[data.RoomID] = state.roomUsers[data.RoomID].filter(function (user) {
            return user.UserID != data.UserID;
        });
        
        state.roomUsers[data.RoomID].push(data);
    },
    
    MSG_ROOM_USER_LEFT(state, data) {
        if(!state.roomUsers[data.RoomID]) {
            return;
        }
        
        state.roomUsers[data.RoomID] = state.roomUsers[data.RoomID].filter(function (user) {
            return user.UserID != data.UserID;
        });
    },

    MSG_AUTOMATCH_STATUS(state, data) {
        state.auth.user.automatch = data.InQueue;
    },
    
    MSG_GAME_STARTED(state, data) {
        var game = state.activeGames.find(function(game) {
            return game.ID == data.ID;
        });
        
        if(game && game.Demo) {
            game.Stage = 'playing';
        } else if(!game) {
            state.activeGames.push(data);
        }

        if(!data.Demo && (data.MatchBlack == state.auth.user.userID || data.MatchWhite == state.auth.user.userID)) {
            state.route.router.go({name: 'game', params: {gameID: data.ID}});
        }
    },

    MSG_GAME_FINISHED(state, data) {
        var game = state.openGames.find(function(game) {
            return game.ID == data.GameID;
        });

        if(game) {
            game.Stage = 'finished';
            game.Result = data.Result;
        }

        state.activeGames = state.activeGames.filter(function(game) {
            return game.ID != data.GameID;
        });
    },

    MSG_GAME_DATA(state, data) {
        state.openGames = state.openGames.filter(function(game) {
            return game.ID != data.ID;
        });

        state.openGames.push(data);

        Vue.set(state.gameHasUpdate, data.ID, true);

        mutations.UPDATE_GAME_TIME(state, data.ID);
    },

    MSG_GAME_UPDATE(state, data) {
        var game = state.openGames.find(function(game) {
            return game.ID == data.GameID;
        });

        if(!game) {
            return;
        }

        game.Stage = data.Stage;
        game.Result = data.Result;
        game.Timing = data.Timing;

        if(data.Node) {
            if(!game.Board.Tree) {
                Vue.set(game.Board, 'Tree', []);
            }

            if (!game.Board.Tree[data.Node.ID]) {
                // This value will be needed to detect if a game update created a new node.
                // Useful for determining if a sound should be played.
                Vue.set(game.Board, 'LastInsertedNodeID', data.Node.ID);
                game.Board.Tree.push(data.Node);
            } else {
                game.Board.Tree.$set(data.Node.ID, data.Node);
            }

            game.Board.CurrentNodeID = data.Node.ID;

            if(data.Node.ParentID >= 0) {
                if (!game.Board.Tree[data.Node.ParentID].Children) {
                    Vue.set(game.Board.Tree[data.Node.ParentID], 'Children', []);
                }

                if(game.Board.Tree[data.Node.ParentID].Children.indexOf(data.Node.ID) == -1) {
                    game.Board.Tree[data.Node.ParentID].Children.push(data.Node.ID);
                }
            }
        }

        Vue.set(state.gameHasUpdate, data.GameID, true);

        mutations.UPDATE_GAME_TIME(state, data.GameID);
    },
    
    MSG_LOAD_DIRECT_ROOM(state, room) {
        Vue.set(state.directRooms, room.OtherUserID, {
            RoomID: room.Room.ID,
            OtherUserID: room.OtherUserID,
            IsOnline: room.IsOnline,
            IsActive: room.IsActive
        });
        
        Vue.set(state.roomLogs, room.Room.ID, room.RoomLogs);
        Vue.set(state.roomHasUpdate, room.Room.ID, room.HasUnread);
    },
    
    UPDATE_ROUTE(state, route) {
        Vue.set(state, 'route', route);
    },
    
    TOGGLE_SIDEBAR(state) {
        state.sidebar.open = !state.sidebar.open;
    },
    
    UPDATE_GAME_TIME(state, id) {
        var game = state.openGames.find(function(game) {
            return game.ID == id;
        });

        if(!game || game.Demo || !game.Board.Tree || (!game.Demo && game.Stage == 'finished') ||
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

    OPEN_GAME(state, gameID) {
        var game = state.openGames.find(function(game) {
            return game.ID == gameID;
        });

        if(game && game.Board) {
            return;
        }

        Vue.http.post('/api/games/'+gameID+'/open');
    },

    CLOSE_GAME(state, gameID) {
        Vue.http.post('/api/games/'+gameID+'/close');

        state.openGames = state.openGames.filter(function(game) {
            return game.ID != gameID;
        });
    },
    
    LOAD_ROOM_USERS(state, roomID) {
        if(!roomID || !!state.roomUsers[roomID]) {
            return;
        }

        Vue.http.get('/api/rooms/'+roomID+'/users').then(function(res) {
            Vue.set(state.roomUsers, roomID, res.data);
        });
    },
    
    RELOAD_USER_AVATAR(state) {
        state.auth.user.avatarURL = '/api/users/' + state.auth.user.userID + '/avatar?' + (new Date()).getTime();
    },
    
    LOAD_DIRECT_ROOM(state, userID) {
        Vue.http.post('/api/users/' + userID + '/open-direct').then(function(res) {
            mutations.MSG_LOAD_DIRECT_ROOM(state, res.data);
        }, function() {})
    },
    
    CLEAR_ROOM_UPDATE(state, roomID) {
        Vue.set(state.roomHasUpdate, roomID, false);

        var isDirect = Object.keys(state.directRooms).find(function(userID) {
            return state.directRooms[userID].RoomID == roomID;
        });

        if(isDirect) {
            Vue.http.post('/api/rooms/' + roomID + '/mark-read');
        }
    },
    
    CLEAR_GAME_UPDATE(state, gameID) {
        Vue.set(state.gameHasUpdate, gameID, false);
    }
};

export default new Vuex.Store({
    state,
    mutations
});