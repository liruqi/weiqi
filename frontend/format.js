export function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

export function format_duration(seconds) {
    var sec = Math.ceil(seconds);
    var min = Math.floor(sec / 60);
    var hours = Math.floor(min / 60);
    
    if(sec <= 0) {
        return '00:00';
    }

    sec -= min * 60;
    min -= hours * 60;
    
    var duration = '';
    
    if(hours > 0) {
        duration = pad(hours) + ':';
    }
    
    duration += pad(min) + ":" + pad(sec);
    
    return duration;
}
