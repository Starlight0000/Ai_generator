CREATE TABLE content(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id TEXT NOT NULL,
    prompt TEXT NOT NULL,
    video_paths TEXT,
    image_paths TEXT,
    status TEXT NOT NULL,
    generated_at DATETIME NOT NULL
);

INSERT into content(id,user_id,prompt,video_paths,image_paths,status,generated_at)
VALUES(1,"user1","Create a motivational video about success.","None", "None", "Processing","5")

SELECT * from content
-- TRUNCATE TABLE content
-- DELETE FROM content
-- WHERE id BETWEEN 1 AND 60