import { Howl } from 'howler';

var sounds = {
    'beep': new Howl({src: ['/static/sounds/beep.wav']}),
    'black_stone': new Howl({src: ['/static/sounds/black.mp3', '/static/sounds/black.ogg']}),
    'white_stone': new Howl({src: ['/static/sounds/white.mp3', '/static/sounds/white.ogg']}),
};

export function play_sound(key) {
    var snd = sounds[key];
    if(snd) {
        snd.play();
    }
}
