DROP TABLE IF EXISTS top6000songs;
CREATE TABLE top6000songsWithFav (
    songRank int,
    songArtist VARCHAR(255),
    songTitle VARCHAR(255),
    songYear int,
    songFavoriteMacallan int,
    songFavoriteTom int
);