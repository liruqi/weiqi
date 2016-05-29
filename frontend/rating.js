export function rating_to_rank(rating) {
    var perRank = 100;
    var start = 100;
    var minRank = -20;
    var maxRank = 9;

    var rank = minRank + Math.floor((rating-start)/perRank);

    if(rank >= 0) {
        rank++;
    }

    rank = Math.min(maxRank, rank);
    rank = Math.max(minRank, rank);

    if(rank > 0) {
        return rank + "d";
    }

    return Math.abs(rank) + "k";
}
