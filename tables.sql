-- TABELAS E INDEXES USADOS NO PROJETO:

CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT NOT NULL, email TEXT NOT NULL, hash_password TEXT NOT NULL);

CREATE TABLE IF NOT EXISTS categories (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, id_color INTEGER NOT NULL REFERENCES colors(id), FOREIGN KEY (user_id) REFERENCES users(id));

-- ON DELETE CASCADE -> se uma categoria for deletada, seu respectivo orçamento tbm será
CREATE TABLE IF NOT EXISTS budgets (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL REFERENCES users(id), category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE, amount REAL NOT NULL);

-- ON DELETE SET NULL -> se uma categoria for deletada, o campo category_id(FK) em transactions receberá NULL
CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL REFERENCES users(id), category_id INTEGER REFERENCES categories(id) ON DELETE SET NULL, date TEXT NOT NULL, amount REAL NOT NULL);

CREATE TABLE IF NOT EXISTS colors (id INTEGER PRIMARY KEY AUTOINCREMENT, code TEXT NOT NULL);

CREATE INDEX idx_usr_email ON users(email);

CREATE INDEX idx_usr_username ON users(username);

CREATE INDEX idx_ctg_idColor ON categories(id_color);

CREATE INDEX idx_ctg_usrId ON categories(user_id);

CREATE INDEX idx_bdg_ctgId ON budgets(category_id);

CREATE INDEX idx_trans_ctgId ON transactions(category_id);

CREATE INDEX idx_trans_usrId ON transactions(user_id);

CREATE INDEX idx_trans_year_month ON transactions(strftime('%Y', date), strftime('%m', date));


