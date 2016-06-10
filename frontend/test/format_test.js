import { assert } from 'chai';
import { format_duration } from '../format';

describe('time formating', function() {
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
