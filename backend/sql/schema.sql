CREATE TABLE teams (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(128) NOT NULL,
  short_name VARCHAR(64),
  conference VARCHAR(64),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  UNIQUE KEY uq_team_name (name)
);

CREATE TABLE players (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  team_id BIGINT NOT NULL,
  first_name VARCHAR(64),
  last_name VARCHAR(64),
  bats ENUM('R','L','S'),
  throws ENUM('R','L'),
  position VARCHAR(16),
  class_year VARCHAR(16),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (team_id) REFERENCES teams(id)
);

CREATE TABLE games (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  game_date DATE NOT NULL,
  season_year INT NOT NULL,
  home_team_id BIGINT NOT NULL,
  away_team_id BIGINT NOT NULL,
  home_score INT,
  away_score INT,
  status ENUM('scheduled','final','in_progress') DEFAULT 'final',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (home_team_id) REFERENCES teams(id),
  FOREIGN KEY (away_team_id) REFERENCES teams(id)
);

CREATE TABLE batting_lines (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  game_id BIGINT NOT NULL,
  player_id BIGINT NOT NULL,
  ab INT DEFAULT 0,
  h INT DEFAULT 0,
  _2b INT DEFAULT 0,
  _3b INT DEFAULT 0,
  hr INT DEFAULT 0,
  bb INT DEFAULT 0,
  so INT DEFAULT 0,
  rbi INT DEFAULT 0,
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (player_id) REFERENCES players(id),
  UNIQUE KEY uq_batting_line (game_id, player_id)
);

CREATE TABLE pitching_lines (
  id BIGINT PRIMARY KEY AUTO_INCREMENT,
  game_id BIGINT NOT NULL,
  player_id BIGINT NOT NULL,
  outs_recorded INT DEFAULT 0,
  h INT DEFAULT 0,
  er INT DEFAULT 0,
  bb INT DEFAULT 0,
  so INT DEFAULT 0,
  FOREIGN KEY (game_id) REFERENCES games(id),
  FOREIGN KEY (player_id) REFERENCES players(id),
  UNIQUE KEY uq_pitching_line (game_id, player_id)
);
