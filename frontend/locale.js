import Vue from 'vue';
import i18n from 'vue-i18n';
import * as locale from './../static/locales/en.json';

export default function configLocale() {
    Vue.use(i18n, {
        lang: 'en',
        locales: {
            en: locale
        }
    });
}
