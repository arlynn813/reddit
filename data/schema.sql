PRAGMA foreign_keys = ON;

CREATE TABLE User(
    username TEXT NOT NULL,
    email TEXT NOT NULL,
    picture TEXT NOT NULL,
    id TEXT PRIMARY KEY,  -- will be hashed from username
    UNIQUE(username, email)
);

CREATE TABLE Post(
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id TEXT NOT NULL,  -- users post articles
    FOREIGN KEY(user_id) REFERENCES user(id)
);

CREATE TABLE Vote(
    value INTEGER NOT NULL,  -- -1 for downvote, 1 for upvote
    user_id TEXT NOT NULL,  -- user can only vote once per post
    post_id INTEGER NOT NULL,  -- vote is placed on post
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    FOREIGN KEY(user_id) REFERENCES user(id),
    FOREIGN KEY(post_id) REFERENCES post(id)
);
