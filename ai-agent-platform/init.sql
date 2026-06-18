CREATE TABLE users (id UUID PRIMARY KEY, email TEXT UNIQUE, password_hash TEXT);
CREATE TABLE tasks (id UUID PRIMARY KEY, user_id UUID, status TEXT, created_at TIMESTAMP);
CREATE TABLE agents (id UUID PRIMARY KEY, name TEXT, type TEXT);
CREATE TABLE executions (id UUID PRIMARY KEY, task_id UUID, agent_id UUID, status TEXT);
CREATE TABLE results (id UUID PRIMARY KEY, execution_id UUID, data JSONB);