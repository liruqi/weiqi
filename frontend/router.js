import Vue from 'vue';
import VueRouter from 'vue-router';

Vue.use(VueRouter);

export function config_router() {
    var router = new VueRouter({
        history: true,
        saveScrollPosition: false,
        linkActiveClass: 'active'
    });

    // The router does not automatically scroll to top on route change.
    router.beforeEach(function(transition) {
        if(window.location.hash == '') {
            var wrapper = jQuery('.main-wrapper');
            wrapper.scrollTop(0);
            wrapper.scrollLeft(0);
        }
        
        transition.next();
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
        '/rooms/:room_id': {
            name: 'room',
            component: require('./components/room/room.vue')
        },
        '/users/:user_id': {
            name: 'user',
            component: require('./components/user/profile.vue')
        },
        '/users/:user_id/message': {
            name: 'user_message',
            component: require('./components/user/message.vue')
        },
        '/games': {
            name: 'active_games',
            component: require('./components/active_games.vue')
        },
        '/games/:game_id': {
            name: 'game',
            component: require('./components/game/game.vue')
        },
        '/challenges/:challenge_id': {
            name: 'challenge',
            component: require('./components/challenge/view_challenge.vue')
        },
        '/search/:query': {
            name: 'search',
            component: require('./components/search.vue')
        }
    });

    return router;
}
