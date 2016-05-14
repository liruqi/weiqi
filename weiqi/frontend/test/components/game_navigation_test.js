import Vue from 'vue';
import { setup_test } from '../utils';
import { create_game } from '../fixtures';

setup_test();

describe('game_navigation.vue', function() {
    function get_component() {
        return new Vue({
            components: {'qi-nav': require('./../../components/game/game_navigation.vue')},
            template: '<div><qi-nav v-ref:component :game="game" :is_player="is_player" :has_control="has_control" '
                + ':force_node_id.sync="force_node_id"></qi-nav></div>',
            data() {
                return {
                    game: create_game(),
                    is_player: false,
                    has_control: false,
                    force_node_id: false
                }
            }
        }).$mount();
    }

    it('should render correctly', function(done) {
        var vm = get_component();
        var comp = vm.$refs.component;
        
        comp.$set('expanded.n0', true);
        comp.$set('expanded.n1', true);
        comp.$set('expanded.n2', true);

        comp.$nextTick(function() {
            expect(vm.$el.querySelectorAll('.game-nav-node').length).toBe(3);
            done();
        });
    });

    describe('back-to-game button', function() {
        var tests = [
            ['normal game', false, false, false, true],
            ['demo spectator', true, false, false, true],
            ['demo controller', true, false, true, false]
        ];

        tests.forEach(function(test) {
            it('should show correctly: '+test[0], function (done) {
                var vm = get_component();
                var comp = vm.$refs.component;

                vm.game.is_demo = test[1];
                vm.is_player = test[2];
                vm.has_control = test[3];

                comp.$nextTick(function () {
                    if(test[4]) {
                        expect(comp.$els.back_to_game).toBeTruthy();
                    } else {
                        expect(comp.$els.back_to_game).toBeFalsy();
                    }
                    done();
                });
            });
        });
    });
});