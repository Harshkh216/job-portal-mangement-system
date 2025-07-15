CREATE TABLE jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    location TEXT NOT NULL
);

CREATE TABLE applications (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id INTEGER,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    FOREIGN KEY (job_id) REFERENCES jobs (id)
);

INSERT INTO jobs (title, company, location) VALUES 
('Software Engineer', 'Google', 'Bangalore'),
('Data Analyst', 'Amazon', 'Hyderabad'),
('Web Developer', 'Infosys', 'Pune'),
('AI Engineer', 'TCS', 'Delhi');