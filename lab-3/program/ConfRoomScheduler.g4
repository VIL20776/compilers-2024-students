grammar ConfRoomScheduler;

prog: stat+;

stat:
	reserve NEWLINE			# reserveStat
	| cancel NEWLINE		# cancelStat
	| reschedule NEWLINE	# rescheduleStat
	| 'LISTAR' NEWLINE		# listStat
	| NEWLINE				# blank;

reserve:
	'RESERVAR' ROOM_TYPE ID 'PARA' DATE 'DE' TIME 'A' TIME 'POR' ID 'DESCRIPCION' STRING;
cancel: 'CANCELAR' ID 'PARA' DATE 'DE' TIME 'A' TIME;
reschedule:
	'REPROGRAMAR' ID 'PARA' DATE 'DE' TIME 'A' TIME 'POR' ID 'DESCRIPCION' STRING;

ROOM_TYPE: 'BOARDROOM' | 'TRAININGROOM' | 'MEETINGROOM';
DATE: DIGIT DIGIT '/' DIGIT DIGIT '/' DIGIT DIGIT DIGIT DIGIT;
TIME: DIGIT DIGIT ':' DIGIT DIGIT;
ID: [a-zA-Z0-9]+;
STRING: '"' (~["\r\n])* '"';
COMMENT: '#' ~[\r\n]* -> skip;
NEWLINE: '\r'? '\n';
WS: [ \t]+ -> skip;

fragment DIGIT: [0-9];
