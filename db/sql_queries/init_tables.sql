CREATE TABLE IF NOT EXISTS "user" (id SERIAL PRIMARY KEY,
                                 first_name VARCHAR(100) NOT NULL,
                                 last_name VARCHAR(100) NOT NULL,
                                 phone VARCHAR(50),
                                 email VARCHAR(50),
                                 is_admin BOOLEAN DEFAULT FALSE);

CREATE TABLE IF NOT EXISTS food_report (id SERIAL PRIMARY KEY,
                                        proteins REAL NOT NULL,
                                        fats REAL NOT NULL,
                                        carbohydrates REAL NOT NULL,
                                        calories REAL NOT NULL,
                                        cellulose REAL NOT NULL,
                                        date_report TIMESTAMP DEFAULT NOW(),
                                        user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS body_report (id SERIAL PRIMARY KEY,
                                              weight REAL NOT NULL,
                                              size_waist REAL NOT NULL,
                                              size_chest REAL NOT NULL,
                                              size_thighs REAL NOT NULL,
                                              size_left_biceps REAL NOT NULL,
                                              size_right_biceps REAL NOT NULL,
                                              size_pelvis REAL NOT NULL,
                                              size_buttocks REAL NOT NULL,
                                              date_report TIMESTAMP DEFAULT NOW(),
                                              user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE);

CREATE TABLE IF NOT EXISTS normal_food (id SERIAL PRIMARY KEY,
                                        normal_proteins REAL NOT NULL,
                                        normal_fats REAL NOT NULL,
                                        normal_carbohydrates REAL NOT NULL,
                                        normal_calories REAL NOT NULL,
                                        normal_cellulose REAL NOT NULL,
                                        user_id INTEGER REFERENCES "user"(id) ON DELETE CASCADE);