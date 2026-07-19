from models import User, Brand
from database import users, brands, sales, payouts, withdrawals
from service import SaleService, PayoutService, WithdrawalService
from enums import SaleStatus, PayoutStatus
sale_service = SaleService()
payout_service = PayoutService()
withdrawal_service = WithdrawalService()

john = User(
    id="john_doe",
    name="John Doe"
)

users[john.id] = john

nike = Brand(
    brand_id="brand_1",
    name="Nike"
)

brands[nike.brand_id] = nike

sale = sale_service.create_sale(
    "john_doe",
    "brand_1",
    40
)
payout_service.process_advance_payout()
sale_service.update_sale_status(
    sale.sale_id,
    SaleStatus.APPROVED
)

payout_service.process_final_payout(
    sale.sale_id
)

withdrawal = withdrawal_service.withdraw(
    "john_doe",
    40
)
withdrawal.status = PayoutStatus.FAILED
withdrawal_service.recover_failed_payout(
    withdrawal.withdrawal_id
)


print(users)

print(sales)

print(payouts)

print(withdrawals)