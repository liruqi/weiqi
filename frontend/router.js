import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

export default function configRouter() {
    var router = new VueRouter({
        history: true,
        saveScrollPosition: true,
        linkActiveClass: 'active'
    });
    
    router.map({
        '/': {
            name: 'root',
            component: require('./components/home.vue')
        },
        '/settings': {
            name: 'settings',
            component: function(resolve) {
                require(['./components/settings/settings.vue'], resolve);
            } 
        },
        '/faq': {
            name: 'faq',
            component: function(resolve) {
                require(['./components/faq.vue'], resolve);
            }
        },
        '/rooms/:room_id': {
            name: 'room',
            component: require('./components/room/room.vue')
        },
        '/users/:user_id': {
            name: 'user',
            component: function(resolve) {
                require(['./components/user/profile.vue'], resolve);
            }
        },
        '/users/:user_id/message': {
            name: 'user_message',
            component: function(resolve) {
                require(['./components/user/message.vue'], resolve);
            }
        },
        '/games': {
            name: 'active_games',
            component: function(resolve) {
                require(['./components/active_games.vue'], resolve);
            }
        },
        '/games/:game_id': {
            name: 'game',
            component: function(resolve) {
                require(['./components/game/game.vue'], resolve);
            }
        },
        '/challenges/:challenge_id': {
            name: 'challenge',
            component: function(resolve) {
                require(['./components/challenge/view_challenge.vue'], resolve);
            }
        }
    });

    return router;
}
