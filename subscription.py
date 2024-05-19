from typing import List, Dict
from pydantic import BaseModel
from datetime import datetime, timedelta


class Subscription(BaseModel):
    user_id: str
    plan: str
    amount: float
    start_date: datetime
    next_payment_date: datetime
    interval_days: int


class SubscriptionManager:
    def __init__(self):
        self.subscriptions: List[Subscription] = []

    def add_subscription(self, user_id: str, plan: str, amount: float, interval_days: int):
        start_date = datetime.now()
        next_payment_date = start_date + timedelta(days=interval_days)
        subscription = Subscription(
            user_id=user_id,
            plan=plan,
            amount=amount,
            start_date=start_date,
            next_payment_date=next_payment_date,
            interval_days=interval_days
        )
        self.subscriptions.append(subscription)
        return subscription

    def get_subscriptions(self) -> List[Subscription]:
        return self.subscriptions

    def check_and_process_payments(self, blockchain, node_identifier):
        now = datetime.now()
        for subscription in self.subscriptions:
            if subscription.next_payment_date <= now:
                blockchain.new_transaction(
                    sender=subscription.user_id,
                    recipient=node_identifier,
                    amount=subscription.amount,
                )
                subscription.next_payment_date += timedelta(days=subscription.interval_days)
