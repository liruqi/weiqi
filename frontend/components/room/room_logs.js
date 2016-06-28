import m from 'mithril';

export function controller() {
}

export function view(ctrl) {
    var logs = [];
    var room = {};
    
    return (
        m('.panel.panel-default.flex-column.room-logs.fixed-dropdowns', [
            m('.panel-heading.flex-fixed',
                m('h3.panel-title', [
                    m('i.fa.fa-comments-o'),
                    m('span', (args.title ? args.title : (room.type=='main' ? room.name : $t('room_logs.chat')))),
                ])
            ),
            m('.panel-body.flex-auto', logs.map(function(log) {
                return [
                    m('img.avatar[src=/api/users/' + log.user_id + '/avatar'),
                    m('p.message', [
                        m('span.name', [
                            log.user_display,
                            m('small.text-muted.pull-right[title=]', [
                                m('i.fa.fa-clock-o')
                            ])
                        ]),
                        log.message
                    ])
                ]
            })),
            m('.panel-footer.flex-fixed',
                m('form',
                    m('.input-group', [
                        m('input.form-control[type=text,name=message,autocomplete=off]'),
                        m('.input-group-btn',
                            m('button.btn.btn-success',
                                m('i.fa.fa-plus'))
                        )
                    ])
                )
            )
        ])
    );
}
