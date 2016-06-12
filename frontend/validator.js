import Vue from 'vue';
import VueValidator from 'vue-validator';

export function config_validator() {
    Vue.use(VueValidator);
    
    Vue.validator('display_name', function(val) {
        return /^[a-zA-Z0-9_-]{2,12}$/.test(val)
    });

    Vue.validator('email', function (val/*,rule*/) {
        return /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/.test(val)
    });
}
