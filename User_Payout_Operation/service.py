from datetime import datetime, timedelta
import uuid

from database import users, brands, sales, payouts, withdrawals
from models import Sale, Payout, User, Withdrawal
from enums import SaleStatus, PayoutStatus, PayoutType


class SaleService: 

    def create_sale(self, user_id: str, brand_id: str, earning: float):
        if(user_id not in users) or (brand_id not in brands):
            raise Exception("Invalid user or brand ID")
        if earning<=0:
            raise Exception("Earning must be greater than zero")
        sale=Sale(
            user_id=user_id,
            sale_id=str(uuid.uuid4()),
            brand_id=brand_id,
            earning=earning,
    
)
        sales[sale.sale_id]=sale
        return sale

    def update_sale_status(self, sale_id: str, status: SaleStatus):
        if sale_id not in sales:
            raise Exception("Sale not found")
        sale = sales[sale_id]
        sale.status = status
        return sale


class PayoutService:

    def process_advance_payout(self):
        for sale in sales.values():
            if sale.status!=SaleStatus.PENDING:
                continue
            if sale.advance_paid:
                continue
            advance_amount = sale.earning * 0.10
            user=users[sale.user_id]
            user.wallet_balance += advance_amount
            sale.advance_paid = True
            sale.advance_amount = advance_amount
            payout = Payout(
                user_id=sale.user_id,
                payout_id=str(uuid.uuid4()),
                sale_id=sale.sale_id,
                amount=advance_amount,
                type=PayoutType.ADVANCE,
                status=PayoutStatus.SUCCESS,
                created_at=datetime.now()
            )
            payouts[payout.payout_id] = payout

    def process_final_payout(self, sale_id: str):
        if sale_id not in sales:
            raise Exception("Sale not found")
        
        sale = sales[sale_id]
        if sale.final_paid:
            raise Exception("Final payout already processed for this sale")
        
        user=users[sale.user_id]
        if sale.status == SaleStatus.APPROVED:
            final_amount = sale.earning - sale.advance_amount
            user.wallet_balance += final_amount
            sale.final_paid = True
            payout = Payout(
                user_id=sale.user_id,
                payout_id=str(uuid.uuid4()),
                sale_id=sale.sale_id,
                amount=final_amount,
                type=PayoutType.FINAL,
                status=PayoutStatus.SUCCESS,
                created_at=datetime.now()
            )
            payouts[payout.payout_id] = payout
            
        elif sale.status == SaleStatus.REJECTED:
            adjustment_amount = sale.advance_amount
            user.wallet_balance -= adjustment_amount
            sale.final_paid = True
            payout = Payout(
                user_id=sale.user_id,
                payout_id=str(uuid.uuid4()),
                sale_id=sale.sale_id,
                amount=adjustment_amount,
                type=PayoutType.FINAL,
                status=PayoutStatus.REJECTED,
                created_at=datetime.now()
            )
            payouts[payout.payout_id] = payout
        else:
            raise Exception("Sale is still pending, cannot process final payout")    
            
        return payout


class WithdrawalService:

    def withdraw(self, user_id: str, amount: float):
        if user_id not in users:
            raise Exception("User not found")
        user = users[user_id]
        if amount <= 0:
            raise Exception("Withdrawal amount must be greater than zero")
        if user.wallet_balance < amount:
            raise Exception("Insufficient wallet balance")
        if last_withdrawal_time := user.last_withdrawal_time:
            if datetime.now() - last_withdrawal_time < timedelta(days=1):
                raise Exception("Withdrawal can only be made once in 24 hours")
         
        user.wallet_balance -= amount
        user.last_withdrawal_time = datetime.now()
        withdrawal = Withdrawal(
            user_id=user_id,
            withdrawal_id=str(uuid.uuid4()),
            amount=amount,
            status=PayoutStatus.PENDING,
            requested_at=datetime.now()
        )
        withdrawals[withdrawal.withdrawal_id] = withdrawal
        return withdrawal        
    

    def recover_failed_payout(self, withdrawal_id: str):
        if withdrawal_id not in withdrawals:
            raise Exception("Withdrawal not found")
        withdrawal = withdrawals[withdrawal_id]
        
        if withdrawal.status not in (
        PayoutStatus.FAILED,
        PayoutStatus.REJECTED,
        PayoutStatus.CANCELLED,
    ):
            raise Exception("Recovery not allowed")
        if withdrawal.refund_processed:
            raise Exception("Refund already processed")

        user = users[withdrawal.user_id]
        user.wallet_balance += withdrawal.amount
        withdrawal.refund_processed = True

        return user.wallet_balance