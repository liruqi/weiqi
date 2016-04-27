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
            component: require('./components/settings/settings.vue')
        },
        '/faq': {
            name: 'faq',
            component: require('./components/faq.vue')
        },
        '/rooms/:roomID': {
            name: 'room',
            component: require('./components/room/room.vue')
        },
        '/users/:userID': {
            name: 'user',
            component: require('./components/user/profile.vue')
        },
        '/users/:userID/message': {
            name: 'userMessage',
            component: require('./components/user/message.vue')
        },
        '/games': {
            name: 'activeGames',
            component: require('./components/active_games.vue')
        },
        '/games/:gameID': {
            name: 'game',
            component: require('./components/game/game.vue')
        },
        '/password-reset-confirm/:status': {
            component: require('./components/password_reset_confirm.vue')
        }
    });

    return router;
}
