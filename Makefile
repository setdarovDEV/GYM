pg_con:
	#command

build:
	image create
	run container


restart:
	container delete
	image delete
	image create
	run container


