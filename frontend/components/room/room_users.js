import m from 'mithril';
import { load_room_users } from '../../vuex/actions_m';

export function controller(args) {
   load_room_users(args.state, args.room_id());
}

export function view(ctrl, args) {
    var users = args.state.room_users[args.room_id()] || [];
    var $t = function() {};

    return (
        m('.panel.panel-default.room-users.fixed-dropdowns',
            m('table.table.table-hover.table-striped.table-condensed.flex-auto',
                m('thead',
                    m('tr', [
                        m('th', $t('room_users.username')),
                        m('th', $t('room_users.rank'))
                    ]),
                    m('tbody', users.map(function(user) {
                        return (
                            m('tr',
                                m('td', user.user_display),
                                m('td', user.user_rating),
                        ));
                    }))))));
}
