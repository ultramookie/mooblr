CREATE TABLE mooblr (
	id		BIGINT UNSIGNED,
	title		VARCHAR(1024),
	text		TEXT,
	timestamp	DATETIME,
	url		VARCHAR(1024),
	slug		VARCHAR(1024),
	PRIMARY KEY (id)
);
