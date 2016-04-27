import Vue from 'vue';
import i18n from 'vue-i18n';

export function setupTest() {
    Vue.use(i18n, {
        lang: 'en',
        locales: {}
    });
}

export function trigger(target, event, process) {
    var e = document.createEvent('HTMLEvents');
    e.initEvent(event, true, true);
    
    if(process) {
        process(e)
    }
    
    target.dispatchEvent(e);
    
    return e;
}
