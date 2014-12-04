create table sessions (
    session_id char(128) NOT NULL,
    atime timestamp NOT NULL default CURRENT_TIMESTAMP,
    data text,
    UNIQUE KEY session_id (session_id)
);