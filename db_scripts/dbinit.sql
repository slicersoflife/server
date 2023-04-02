CREATE DATABASE IF NOT EXISTS dev;

USE dev;

CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    phone VARCHAR(20) NOT NULL,
    username VARCHAR(20),
    display_name VARCHAR(50),
    profile_picture_url VARCHAR(255) NULL,
    UNIQUE INDEX users_display_name (display_name ASC)
);

CREATE TABLE IF NOT EXISTS friend_requests (
    id_requests uuid PRIMARY KEY NOT NULL DEFAULT gen_random_uuid(),
    from_user_id INT NOT NULL,
    to_user_id INT NOT NULL,
    status ENUM("accepted", "pending") NOT NULL,
    FOREIGN KEY (from_user_id) REFERENCES users(id),
    FOREIGN KEY (to_user_id) REFERENCES users(id)
);

