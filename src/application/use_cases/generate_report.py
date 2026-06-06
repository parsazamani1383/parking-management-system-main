from datetime import datetime, timedelta


class GenerateReport:
    def __init__(self, session_repo, receipt_repo, spot_repo):
        self.session_repo = session_repo
        self.receipt_repo = receipt_repo
        self.spot_repo = spot_repo

    def get_daily_financial_report(self, date: datetime):
        start_of_day = date.replace(hour=0, minute=0, second=0)
        end_of_day = date.replace(hour=23, minute=59, second=59)

        receipts = self.receipt_repo.get_receipts_in_range(start_of_day, end_of_day)
        total_income = sum(r.amount for r in receipts)

        return {
            "date": date.date().isoformat(),
            "total_income": total_income,
            "transaction_count": len(receipts)
        }

    def get_traffic_report(self, start_date: datetime, end_date: datetime, vehicle_type: str = None):
        sessions = self.session_repo.get_sessions_in_range(start_date, end_date)

        if vehicle_type:
            sessions = [s for s in sessions if s.vehicle_type == vehicle_type]

        entries = len(sessions)
        exits = len([s for s in sessions if s.status == 'completed'])

        return {
            "period": f"{start_date.date()} to {end_date.date()}",
            "vehicle_type": vehicle_type if vehicle_type else "all",
            "entries": entries,
            "exits": exits
        }

    def get_occupancy_status(self):
        capacity_info = self.spot_repo.get_capacity_stats()

        return {
            "total_capacity": capacity_info["total"],
            "occupied_spots": capacity_info["occupied"],
            "free_spots": capacity_info["available"]
        }

    def get_operator_performance(self, operator_id: int, start_date: datetime, end_date: datetime):
        sessions = self.session_repo.get_sessions_by_operator_and_range(operator_id, start_date, end_date)

        return {
            "operator_id": operator_id,
            "total_actions": len(sessions),
            "completed_exits": len([s for s in sessions if s.status == 'completed'])
        }
