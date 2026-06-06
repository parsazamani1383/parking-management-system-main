from datetime import datetime


class ManageShift:
    def __init__(self, shift_repo):
        self.shift_repo = shift_repo

    def open_shift(self, operator_id: int):
        active_shift = self.shift_repo.get_active_shift_by_operator(operator_id)
        if active_shift:
            raise Exception("Operator already has an active shift")

        return self.shift_repo.start_shift(operator_id)

    def close_shift(self, shift_id: int):
        shift = self.shift_repo.get_shift_by_id(shift_id)
        if not shift or shift.shift_status == 'closed':
            raise Exception("Invalid or already closed shift")

        self.shift_repo.end_shift(shift_id)
        return True
