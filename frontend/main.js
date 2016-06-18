import Vue from 'vue';
import VueResource from 'vue-resource';
import bootbox from 'bootbox';
import toastr from 'toastr';
import { config_router } from './router';
import { config_locale } from './locale';
import { connect } from './socket';
import { config_validator } from './validator';
import { fix_dropdowns } from './fixed_dropdowns';

window.jQuery = require('jquery');
require('bootstrap-sass');
require('select2');
require('babel-polyfill');

const App = Vue.extend(require('./app.vue'));

Vue.use(VueResource);
Vue.http.options.emulateJSON = true;

Vue.config.debug = true;

connect();
config_locale();
config_validator();
const router = config_router();

bootbox.setDefaults({
    size: 'small'
});

toastr.options.newestOnTop = true;
toastr.options.positionClass = 'toast-top-center';

fix_dropdowns();

Vue.component('qi-header', require('./components/header.vue'));
Vue.component('qi-sidebar', require('./components/sidebar.vue'));
Vue.component('qi-sign-in', require('./components/sign_in/sign_in.vue'));
Vue.component('qi-user-context', require('./components/user_context.vue'));
Vue.component('qi-username-rank', require('./components/username_rank.vue'));
Vue.component('qi-rating-rank', require('./components/rating_rank.vue'));
Vue.component('qi-play-dialog', require('./components/play_dialog.vue'));
Vue.component('qi-board', require('./components/board.vue'));
Vue.component('qi-room-users', require('./components/room/room_users.vue'));
Vue.component('qi-room-logs', require('./components/room/room_logs.vue'));
Vue.component('qi-disconnected', require('./components/disconnected.vue'));
Vue.component('qi-page-load-spinner', require('./components/page_load_spinner.vue'));
Vue.component('qi-recaptcha', require('./components/recaptcha.vue'));
Vue.component('qi-create-demo', require('./components/create_demo.vue'));
Vue.component('qi-upload-sgf', require('./components/upload_sgf.vue'));
Vue.component('qi-challenge', require('./components/challenge/challenge_dialog.vue'));
Vue.component('qi-game-type', require('./components/game/game_type.vue'));
Vue.component('qi-game-speed', require('./components/game/game_speed.vue'));
Vue.component('qi-user-last-activity', require('./components/user/last_activity.vue'));

router.start(App, 'body > app');
