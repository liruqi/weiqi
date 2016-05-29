export function pad(n) {
    return (n < 10) ? ("0" + n) : n;
}

export function format_duration(seconds) {
    var sec = Math.ceil(seconds);
    var min = Math.floor(sec / 60);
    
    if(sec <= 0) {
        return '00:00';
    }

    sec -= min * 60;
    
    return pad(Math.round(min)) + ":" + pad(Math.round(sec));
}
