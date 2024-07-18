
class Reservation:
    def __init__(self, room_type, id, date, start_time, end_time, requester, description):
        self.room_type = room_type
        self.id = id
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.requester = requester
        self.description = description

    def overlaps(self, other):
        return self.date == other.date and not (self.end_time <= other.start_time or self.start_time >= other.end_time)

    def __repr__(self):
        return (f"Room Type: {self.room_type}, Room ID: {self.id}, Date: {self.date.strftime('%d/%m/%Y')}, "
                f"Time: {self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')}, "
                f"Requester: {self.requester}, Description: {self.description}")
