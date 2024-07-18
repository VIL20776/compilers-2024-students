import sys
from antlr4 import *
from ConfRoomSchedulerLexer import ConfRoomSchedulerLexer
from ConfRoomSchedulerParser import ConfRoomSchedulerParser
from ConfRoomSchedulerListener import ConfRoomSchedulerListener

from datetime import datetime

from Types import Reservation

reservations = []

class ConfRoomSchedulerSemanticChecker(ConfRoomSchedulerListener):
    MAX_USAGE_HOURS = 4

    def enterReserveStat(self, ctx):
        tokens = ctx.reserve()
        try:
            room_type = tokens.getChild(1).getText()
            room_id = tokens.getChild(2).getText()
            date = datetime.strptime(tokens.getChild(4).getText(), '%d/%m/%Y')
            start_time = datetime.strptime(tokens.getChild(6).getText(), '%H:%M')
            end_time = datetime.strptime(tokens.getChild(8).getText(), '%H:%M')
            requester = tokens.getChild(10).getText()
            description = tokens.getChild(12).getText().strip('"')
        except ValueError as e:
            raise ValueError(f"Invalid date or time format: {e}")

        if start_time >= end_time:
            raise ValueError("Start time must be less than end time")

        if (end_time - start_time).total_seconds() / 3600 > self.MAX_USAGE_HOURS:
            raise ValueError(f"Reservation exceeds maximum usage time of {self.MAX_USAGE_HOURS} hours")

        new_reservation = Reservation(room_type, room_id, date, start_time, end_time, requester, description)
        for reservation in reservations:
            if reservation.overlaps(new_reservation):
                raise ValueError(f"Reservation overlaps with an existing reservation: {reservation}")

        reservations.append(new_reservation)

    def enterCancelStat(self, ctx):
        tokens = ctx.cancel()
        room_id = tokens.getChild(1).getText()
        date = datetime.strptime(tokens.getChild(3).getText(), '%d/%m/%Y')
        start_time = datetime.strptime(tokens.getChild(5).getText(), '%H:%M')
        end_time = datetime.strptime(tokens.getChild(7).getText(), '%H:%M')

        for reservation in reservations:
            if (reservation.id == room_id and reservation.date == date and
                reservation.start_time == start_time and reservation.end_time == end_time):
                reservations.remove(reservation)
                return

        raise ValueError("No matching reservation found to cancel")

    def enterRescheduleStat(self, ctx):
        tokens = ctx.reschedule()
        try:
            room_id = tokens.getChild(1).getText()
            new_date = datetime.strptime(tokens.getChild(3).getText(), '%d/%m/%Y')
            new_start_time = datetime.strptime(tokens.getChild(5).getText(), '%H:%M')
            new_end_time = datetime.strptime(tokens.getChild(7).getText(), '%H:%M')
            requester = tokens.getChild(9).getText()
            description = tokens.getChild(11).getText().strip('"')
        except ValueError as e:
            raise ValueError(f"Invalid date or time format: {e}")

        if new_start_time >= new_end_time:
            raise ValueError("New start time must be less than new end time")

        if (new_end_time - new_start_time).total_seconds() / 3600 > self.MAX_USAGE_HOURS:
            raise ValueError(f"New reservation exceeds maximum usage time of {self.MAX_USAGE_HOURS} hours")

        # Find and remove the old reservation
        old_reservation = None
        for reservation in reservations:
            if (reservation.id == room_id):
                old_reservation = reservation
                break
        if old_reservation is None:
            raise ValueError("No matching reservation found to reschedule")

        reservations.remove(old_reservation)

        # Check for overlaps with the new reservation
        new_reservation = Reservation(old_reservation.room_type, room_id, new_date, new_start_time, new_end_time, requester, description)
        for reservation in reservations:
            if reservation.overlaps(new_reservation):
                raise ValueError(f"New reservation overlaps with an existing reservation: {reservation}")

        reservations.append(new_reservation)

    def enterListStat(self, ctx):
        list_reservations()

def list_reservations():
    for reservation in reservations:
        print(reservation)

def main(argv):
    try:
        input_stream = FileStream(argv[1])
        lexer = ConfRoomSchedulerLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = ConfRoomSchedulerParser(stream)
        tree = parser.prog()
        semantic_checker = ConfRoomSchedulerSemanticChecker()
        walker = ParseTreeWalker()
        walker.walk(semantic_checker, tree)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main(sys.argv)
