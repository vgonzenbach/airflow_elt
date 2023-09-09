
songplay_table_insert = """
    SELECT 
        md5(e.sessionid || e.ts) AS songplay_id,
    	timestamp 'epoch' + ts/1000 * interval '1 second' AS start_time,
    	userid AS user_id,
        level,
        s.song_id AS song_id,
       	s.artist_id AS artist_id,
        sessionid AS session_id,
        location,
        useragent AS user_agent
    FROM staging_events AS e
    JOIN staging_songs AS s
    	ON e.song = s.title
    ORDER BY start_time;
"""
user_table_insert = """
    SELECT DISTINCT userid::INTEGER , firstname, lastname, gender, level
    FROM staging_events
    WHERE TRIM(userid) != '';
"""
song_table_insert = """
    SELECT 
        DISTINCT song_id, 
        title,
        artist_id,
        year,
        duration
    FROM staging_songs;
"""
artist_table_insert = """
    SELECT 
    	DISTINCT artist_id, 
        artist_name,
        artist_location,
        artist_latitude,
        artist_longitude
    FROM staging_songs;
"""
time_table_insert = """
    SELECT 
    	timestamp 'epoch' + ts/1000 * interval '1 second' AS start_time,
        EXTRACT(HOUR FROM start_time) AS hour,
        EXTRACT(DAY FROM start_time) AS day,
        EXTRACT(WEEK FROM start_time) AS week,
        EXTRACT(MONTH FROM start_time) AS month,
        EXTRACT(YEAR FROM start_time) AS year,
        EXTRACT(DOW FROM start_time) AS weekday
    FROM staging_events
    ORDER BY start_time;
"""