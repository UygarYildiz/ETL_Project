
CREATE TABLE users (
    id serial PRIMARY KEY,
    name VARCHAR (100) NOT NULL,
    username VARCHAR (50) NOT NULL,
    city VARCHAR (100) NOT NULL,
    email VARCHAR (100) NOT NULL,
    phone VARCHAR (20) NOT NULL,
    website VARCHAR (100) NOT NULL,
    company_name VARCHAR (100) NOT NULL
);

CREATE TABLE posts(
    id serial PRIMARY KEY,
    user_id INT REFERENCES users(id),
    title VARCHAR (200) NOT NULL,
    body TEXT NOT NULL
    
);
CREATE TABLE comments(
    id serial PRIMARY KEY,
    post_id INT REFERENCES posts(id),
    name VARCHAR (100) NOT NULL,
    email VARCHAR (100) NOT NULL,
    body TEXT NOT NULL
);

