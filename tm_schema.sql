drop database if exists task_manager;
create database task_manager;
use task_manager;

create table user (
	user_id int auto_increment primary key,
	username varchar(50) unique not null,
	password varchar(60) unique not null
);

create table board (
	board_id int auto_increment primary key,
	user_id int not null,
	name varchar(50) not null,
    
    foreign key (user_id) references user(user_id)
);

create table category (
	category_id int auto_increment primary key,
	board_id int not null,
	name varchar(50) not null,
	position int not null,
    
    foreign key (board_id) references board(board_id)
);

create table task (
	task_id int auto_increment primary key,
	category_id int not null,
	title varchar(100) not null,
	position int not null,
	comment varchar(100) null,
	is_completed boolean default false,
	due_date datetime null,
	created_at timestamp,
    
    foreign key (category_id) references category(category_id)
);

create table user_task(
	user_id int not null, 
    task_id int not null,
    
    FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
    FOREIGN KEY (task_id) REFERENCES task(task_id) ON DELETE CASCADE,
    
    PRIMARY KEY (user_id,task_id) 
);

---------------------------------------------------

INSERT INTO user (username, password) VALUES 
('alice_dev', 'hashed_pass_123'),
('bob_coder', 'hashed_pass_456'),
('charlie_git', 'hashed_pass_789'),
('dana_pixels', 'hashed_pass_012');


INSERT INTO board (user_id, name) VALUES 
(1, 'Chess Game')

INSERT INTO category (board_id, name, position) VALUES 
(1, 'Backlog', 1),
(1, 'Sprint 1', 2),
(1, 'Sprint 2', 3),
(1, 'Sprint 3', 4);

-- category 1 tasks
INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
(1, 'Implement AI opponent using Minimax algorithm', 1, false, '2026-07-15 23:59:59', CURRENT_TIMESTAMP),
(1, 'Add online multiplayer via WebSockets', 2, false, '2026-07-30 23:59:59', CURRENT_TIMESTAMP),
(1, 'Design custom chess piece themes', 3, false, NULL, CURRENT_TIMESTAMP),
(1, 'Save game history to local storage', 4, false, NULL, CURRENT_TIMESTAMP);

-- category 2 tasks
INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
(2, 'Set up rendering for 8x8 grid chessboard', 1, true, '2026-06-05 18:00:00', CURRENT_TIMESTAMP),
(2, 'Define core piece movement logic (Pawn, Rook, Knight)', 2, true, '2026-06-08 18:00:00', CURRENT_TIMESTAMP),
(2, 'Create game initialization state and turn switching', 3, true, '2026-06-10 18:00:00', CURRENT_TIMESTAMP);

-- category 3 tasks 
INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
(3, 'Implement rule checks for Check and Checkmate', 1, false, '2026-06-20 18:00:00', CURRENT_TIMESTAMP),
(3, 'Add special move logic (Castling, En Passant)', 2, false, '2026-06-22 18:00:00', CURRENT_TIMESTAMP),
(3, 'Build basic UI for Captured Pieces sidebar', 3, false, '2026-06-25 18:00:00', CURRENT_TIMESTAMP);

-- category 4 takss
INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
(4, 'Integrate match timer clock (Blitz style)', 1, false, '2026-07-01 12:00:00', CURRENT_TIMESTAMP),
(4, 'Write unit tests for move validation matrix', 2, false, '2026-07-03 12:00:00', CURRENT_TIMESTAMP),
(4, 'Fix UI collision bugs on mobile screen layouts', 3, false, '2026-07-05 12:00:00', CURRENT_TIMESTAMP);


-- assigning 1-2 users to each task

-- Alice and Bob
INSERT INTO user_task (user_id, task_id) VALUES (1, 1), (2, 1);
-- Charlie
INSERT INTO user_task (user_id, task_id) VALUES (3, 2);
-- Dana
INSERT INTO user_task (user_id, task_id) VALUES (4, 3);
-- Alice
INSERT INTO user_task (user_id, task_id) VALUES (1, 4);


INSERT INTO user_task (user_id, task_id) VALUES (4, 5), (1, 5);
INSERT INTO user_task (user_id, task_id) VALUES (2, 6), (3, 6);
INSERT INTO user_task (user_id, task_id) VALUES (3, 7);


INSERT INTO user_task (user_id, task_id) VALUES (2, 8);
INSERT INTO user_task (user_id, task_id) VALUES (1, 9), (3, 9);
INSERT INTO user_task (user_id, task_id) VALUES (4, 10);


INSERT INTO user_task (user_id, task_id) VALUES (2, 11), (4, 11);
INSERT INTO user_task (user_id, task_id) VALUES (3, 12);
INSERT INTO user_task (user_id, task_id) VALUES (4, 13);