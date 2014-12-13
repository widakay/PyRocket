
create table projects(
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(64),
	creator INT,
	description TEXT,
	created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
	objectData TEXT,
	PRIMARY KEY ( id )
);
