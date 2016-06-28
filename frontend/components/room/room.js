import m from 'mithril';
var RoomLogs = require('./room_logs');
var RoomUsers = require('./room_users');

export function controller(args) {
    this.state = args.state;
    this.room_id = m.prop(args.room_id || m.route.param('room_id'));
}

export function view(ctrl) {
    return (
        m('.room-page',
            m('section.content',
                m('.row', [
                    m('.flex-column.col-sm-9.col-lg-10', m.component(RoomLogs, {state: ctrl.state, room_id: ctrl.room_id})),
                    m('.flex-column.col-sm-3.col-lg-2', m.component(RoomUsers, {state: ctrl.state, room_id: ctrl.room_id}))
                ]))));
}
