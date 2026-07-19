from dataclasses import dataclass, field
from datetime import datetime

from enums import PayoutStatus, PayoutType, SaleStatus
@dataclass
class User:
    id:str
    name:str
    wallet_balance:float=0
    last_withdrawal_time:datetime=None
    
    
@dataclass    
class Sale:
    user_id:str
    sale_id:str
    brand_id:str
    earning:float
    status: SaleStatus = SaleStatus.PENDING
    advance_paid:bool=False
    advance_amount:float=0
    final_paid:bool=False
    created_at: datetime = field(default_factory=datetime.now)
    
@dataclass
class Payout:
    user_id:str
    payout_id:str
    sale_id:str
    amount:float
    type:PayoutType
    status:PayoutStatus
    created_at:datetime

@dataclass
class Withdrawal:
    user_id:str
    withdrawal_id:str
    amount:float
    status:PayoutStatus
    requested_at: datetime = field(default_factory=datetime.now)
    refund_processed: bool = False

@dataclass
class Brand:
    brand_id:str
    name:str
  