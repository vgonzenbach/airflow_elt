CREATE TABLE public.artists (
  artist_id VARCHAR(19),
  name VARCHAR(256),
  location VARCHAR(256),
  latitude FLOAT4,
  longitude FLOAT4
);

CREATE TABLE public.songplays (
  songplay_id varchar(32) NOT NULL,
  start_time TIMESTAMP,
  user_id INT,
  level VARCHAR(4),
  song_id VARCHAR(19),
  artist_id VARCHAR(19),
  session_id INTEGER,
  location VARCHAR(256),
  user_agent VARCHAR(512)
);

CREATE TABLE public.songs (
  song_id VARCHAR(19),
  title VARCHAR(256),
  artist_id VARCHAR(19),
  year SMALLINT,
  duration FLOAT8
);

CREATE TABLE public.staging_events (
    artist        VARCHAR(256),
    auth          VARCHAR(20),
    firstName     VARCHAR(256),
    gender        CHAR(1),
    itemInSession INTEGER,
    lastName      VARCHAR(256),
    length        FLOAT,
    level         VARCHAR(10),
    location      VARCHAR(256),
    method        VARCHAR(10),
    page          VARCHAR(50),
    registration  BIGINT,
    sessionId     INTEGER,
    song          VARCHAR(256),
    status        INTEGER,
    ts            BIGINT,
    userAgent     VARCHAR(512),
    userId        INT
);

CREATE TABLE public.staging_songs (
    artist_id        VARCHAR(19),
    artist_latitude  FLOAT,
    artist_location  VARCHAR(256),
    artist_longitude FLOAT,
    artist_name      VARCHAR(256),
    duration         FLOAT,
    num_songs        INTEGER,
    song_id          VARCHAR(19),
    title            VARCHAR(256),
    year             INTEGER
);

CREATE TABLE public.times (
  start_time TIMESTAMP sortkey,
  hour SMALLINT,
  day SMALLINT,
  week SMALLINT,
  month SMALLINT,
  year SMALLINT,
  weekday SMALLINT
);

CREATE TABLE users (
  user_id INTEGER,
  first_name VARCHAR(20),
  last_name VARCHAR(15),
  gender CHAR(1),
  level VARCHAR(4)
);
