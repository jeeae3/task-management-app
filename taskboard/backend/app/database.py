import sqlite3


class Database:
    """
    Creates SQLite3 database for task management app
    : populate_db_default : populates the database with some pre-generated data
    """
    def __init__(self, database: str = "task_management_app"):
        # create database and tables
        self._database = database
        self._ensure_tables()

    def _ensure_tables(self):
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS board (
            board_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            
            FOREIGN KEY (user_id) REFERENCES user(user_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS category (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            board_id INT NOT NULL,
            name TEXT NOT NULL,
            position INTEGER NOT NULL,
            
            FOREIGN KEY (board_id) REFERENCES board(board_id)
        );  
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS task (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            position INTEGER NOT NULL,
            comment TEXT,
            is_completed INTEGER DEFAULT 0,
            due_date TEXT,
            created_at TEXT,
            
            FOREIGN KEY (category_id) REFERENCES category(category_id)
        );
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_task(
            user_id INTEGER NOT NULL, 
            task_id INTEGER NOT NULL,
            
            FOREIGN KEY (user_id) REFERENCES user(user_id) ON DELETE CASCADE,
            FOREIGN KEY (task_id) REFERENCES task(task_id) ON DELETE CASCADE,
            
            PRIMARY KEY (user_id,task_id) 
        );
        """)
        conn.commit()
        conn.close()

    def populate_db_default(self):
        conn = sqlite3.connect(self._database)
        cursor = conn.cursor()

        # Empty and remake current tables
        cursor.execute("DROP TABLE IF EXISTS user")
        cursor.execute("DROP TABLE IF EXISTS board")
        cursor.execute("DROP TABLE IF EXISTS category")
        cursor.execute("DROP TABLE IF EXISTS task")
        cursor.execute("DROP TABLE IF EXISTS user_task")

        self._ensure_tables()

        # Populate tables with pre-generated default data
        cursor.execute("""
        INSERT INTO user (username, password) VALUES 
        ('alice_dev', 'hashed_pass_123'),
        ('bob_coder', 'hashed_pass_456'),
        ('charlie_git', 'hashed_pass_789'),
        ('dana_pixels', 'hashed_pass_012');
        """)
        cursor.execute("""
        INSERT INTO board (user_id, name) VALUES 
        (1, 'Chess Game')
        """)
        cursor.execute("""
        INSERT INTO category (board_id, name, position) VALUES 
        (1, 'Backlog', 1),
        (1, 'Sprint 1', 2),
        (1, 'Sprint 2', 3),
        (1, 'Sprint 3', 4);
        """)
        cursor.execute("""
        INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
        (1, 'Implement AI opponent using Minimax algorithm', 1, false, '2026-07-15 23:59:59', CURRENT_TIMESTAMP),
        (1, 'Add online multiplayer via WebSockets', 2, false, '2026-07-30 23:59:59', CURRENT_TIMESTAMP),
        (1, 'Design custom chess piece themes', 3, false, NULL, CURRENT_TIMESTAMP),
        (1, 'Save game history to local storage', 4, false, NULL, CURRENT_TIMESTAMP);
        """)
        cursor.execute("""
        INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
        (2, 'Set up rendering for 8x8 grid chessboard', 1, true, '2026-06-05 18:00:00', CURRENT_TIMESTAMP),
        (2, 'Define core piece movement logic (Pawn, Rook, Knight)', 2, true, '2026-06-08 18:00:00', CURRENT_TIMESTAMP),
        (2, 'Create game initialization state and turn switching', 3, true, '2026-06-10 18:00:00', CURRENT_TIMESTAMP);
        """)
        cursor.execute("""
        INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
        (3, 'Implement rule checks for Check and Checkmate', 1, false, '2026-06-20 18:00:00', CURRENT_TIMESTAMP),
        (3, 'Add special move logic (Castling, En Passant)', 2, false, '2026-06-22 18:00:00', CURRENT_TIMESTAMP),
        (3, 'Build basic UI for Captured Pieces sidebar', 3, false, '2026-06-25 18:00:00', CURRENT_TIMESTAMP);
        """)
        cursor.execute("""
        INSERT INTO task (category_id, title, position, is_completed, due_date, created_at) VALUES
        (4, 'Integrate match timer clock (Blitz style)', 1, false, '2026-07-01 12:00:00', CURRENT_TIMESTAMP),
        (4, 'Write unit tests for move validation matrix', 2, false, '2026-07-03 12:00:00', CURRENT_TIMESTAMP),
        (4, 'Fix UI collision bugs on mobile screen layouts', 3, false, '2026-07-05 12:00:00', CURRENT_TIMESTAMP);
        """)
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (1, 1), (2, 1);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (3, 2);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (4, 3);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (1, 4);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (4, 5), (1, 5);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (2, 6), (3, 6);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (3, 7);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (2, 8);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (1, 9), (3, 9);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (4, 10);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (2, 11), (4, 11);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (3, 12);")
        cursor.execute("INSERT INTO user_task (user_id, task_id) VALUES (4, 13);")
        conn.commit()
        conn.close()

    def get_database(self):
        # Returns database name
        return self._database
