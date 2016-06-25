import { assert } from 'chai';
import { format_duration, format_coordinates } from '../format';

describe('format_duration', function() {
    it('should format days', function() {
        assert.equal(format_duration(3600 * 24), '1d 00:00');
    });

    it('should skip seconds when there are days', function() {
        assert.equal(format_duration(3600*25 + 30*60 + 10), '1d 01:30');
    });
    
    it('should not display days when there are none', function() {
        assert.equal(format_duration(3600*13 + 30*60 + 10), '13:30:10');
    });
    
    it('should zero-pad hours, minutes and seconds', function() {
        assert.equal(format_duration(3600 + 3*60 + 5), '01:03:05');
    });
    
    it('should not display hours when there are none', function() {
        assert.equal(format_duration(3*60 + 5), '03:05');
    });
    
    it('should always display minutes', function() {
        assert.equal(format_duration(5), '00:05');
    });
    
    it('should not display below-zero values', function() {
        assert.equal(format_duration(-5), '00:00');
    });
});

describe('format_coordinates', function() {
    it('should wrap coordinates in a <span>', function() {
        assert.equal(format_coordinates('Test text a1 h10 t19 more text.'),
            'Test text <span>a1</span> <span>h10</span> <span>t19</span> more text.')
    });
    
    it('should add css classes', function() {
        assert.equal(format_coordinates('a1', 'coord'), '<span class="coord">a1</span>');
    });
    
    it('should not format invalid coordinates', function() {
        assert.equal(format_coordinates('a0 j10 k1', 'coord', 9), 'a0 j10 k1');
    });
});
