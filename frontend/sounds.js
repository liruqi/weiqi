import { Howl, Howler } from 'howler';

var sounds = {
    'beep': new Howl({src: ['/static/sounds/beep.wav']}),
    'black_stone': new Howl({src: ['/static/sounds/black.mp3', '/static/sounds/black.ogg'], volume: 0.8}),
    'white_stone': new Howl({src: ['/static/sounds/white.mp3', '/static/sounds/white.ogg'], volume: 0.8}),
    'count_10': new Howl({src: ['/static/sounds/countdown/10.m4a'], volume: 0.5}),
    'count_9': new Howl({src: ['/static/sounds/countdown/09.m4a'], volume: 0.5}),
    'count_8': new Howl({src: ['/static/sounds/countdown/08.m4a'], volume: 0.5}),
    'count_7': new Howl({src: ['/static/sounds/countdown/07.m4a'], volume: 0.5}),
    'count_6': new Howl({src: ['/static/sounds/countdown/06.m4a'], volume: 0.5}),
    'count_5': new Howl({src: ['/static/sounds/countdown/05.m4a'], volume: 0.5}),
    'count_4': new Howl({src: ['/static/sounds/countdown/04.m4a'], volume: 0.5}),
    'count_3': new Howl({src: ['/static/sounds/countdown/03.m4a'], volume: 0.5}),
    'count_2': new Howl({src: ['/static/sounds/countdown/02.m4a'], volume: 0.5}),
    'count_1': new Howl({src: ['/static/sounds/countdown/01.m4a'], volume: 0.5}),
    'count_0': new Howl({src: ['/static/sounds/countdown/00.m4a'], volume: 0.5}),
};

Howler.volume(0.8);

export function play_sound(key) {
    var snd = sounds[key];
    if(snd) {
        snd.play();
    }
}
