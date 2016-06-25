import moment from 'moment';
var link_html = require('linkifyjs/html');

export function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

export function format_duration(seconds) {
    var sec = Math.ceil(seconds);
    var min = Math.floor(sec / 60);
    var hours = Math.floor(min / 60);
    var days = Math.floor(hours / 24);
    
    if(sec <= 0) {
        return '00:00';
    }

    sec -= min * 60;
    min -= hours * 60;
    hours -= days * 24;
    
    var duration = '';
    
    if(days > 0) {
        duration += days + 'd ' + pad(hours) + ':';
    } else if(hours > 0) {
        duration = pad(hours) + ':';
    }
    
    duration += pad(min);
    
    if(days == 0) {
        duration += ":" + pad(sec);
    }
    
    return duration;
}

export function format_datetime(ts) {
    return moment.utc(ts).local().format('YYYY-MM-DD HH:mm')
}

export function format_time(ts) {
    return moment.utc(ts).local().format('HH:mm')
}

export function format_from_now(ts) {
    return moment.utc(ts).fromNow();
}

export function linkify(text) {
    return link_html(text, {
        target: function(href, type) {
            if(type != 'url' || /(https?:\/\/)(www\.)?weiqi\.gs/.test(href)) {
                return null;
            }
            return '_blank';
        }
    });
}
