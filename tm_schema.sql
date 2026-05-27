drop database if exists task_manager;
create database task_manager;
use task_manager;

create table user (
	user_id int auto_increment primary key,
	username varchar(50) unique not null,
	password varchar(50) unique not null
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



