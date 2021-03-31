PRAGMA foreign_keys = ON;

CREATE TABLE user(
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    id TEXT PRIMARY KEY,  -- will be hashed from username
    UNIQUE(username, email)
);

CREATE TABLE post(
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INTEGER NOT NULL,  -- users post articles
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE vote(
    value INTEGER NOT NULL,  -- -1 for downvote, 1 for upvote
    user_id INTEGER NOT NULL,  -- user can only vote once per post
    post_id INTEGER NOT NULL,  -- vote is placed on post
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(post_id) REFERENCES post(id)
);
