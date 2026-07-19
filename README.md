# User Payout Management System

A backend system for managing affiliate user payouts. The system allows users to earn advance payouts on pending sales, receive final payouts after approval, withdraw wallet balance, and recover failed withdrawals.

## Features

- Create and manage sales
- Advance payout (10% of pending sale earnings)
- Final payout after sale approval
- Wallet balance management
- Withdrawal requests
- Failed withdrawal recovery
- REST APIs using Flask
- In-memory database for data storage

---

## Tech Stack

- Python 3
- Flask
- UUID
- Datetime

---

## Project Structure

```
User_Payout_Operation/
│── api.py             # Flask REST APIs
│── app.py             # Sample execution and testing
│── service.py         # Business logic
│── models.py          # Data models
│── enums.py           # Enums
│── database.py        # In-memory database
│── requirements.txt
│── README.md
```

---

## System Design

```
                Client
                   │
                   ▼
             Flask REST API
                   │
        ┌──────────┼──────────┐
        ▼          ▼          ▼
  SaleService  PayoutService WithdrawalService
                   │
                   ▼
           In-Memory Database
```

---

## Business Flow

1. User creates a sale.
2. Every pending sale is eligible for a **10% advance payout**.
3. If the sale is approved:
   - Remaining payout is credited to the wallet.
4. If the sale is rejected:
   - Previously paid advance amount is recovered.
5. User can request withdrawal from wallet.
6. If withdrawal fails, the amount is refunded back to the wallet.

---

## API Endpoints

### Create Sale

```
POST /sales
```

Request

```json
{
    "user_id": "john_doe",
    "brand_id": "brand_1",
    "earning": 500
}
```

---

### Update Sale Status

```
PUT /sales/<sale_id>/status
```

Request

```json
{
    "status": "approved"
}
```

Possible values

- approved
- rejected

---

### Process Advance Payout

```
POST /payouts/advance
```

---

### Process Final Payout

```
POST /payouts/final/<sale_id>
```

---

### Withdraw Money

```
POST /withdraw
```

Request

```json
{
    "user_id": "john_doe",
    "amount": 100
}
```

---

### Recover Failed Withdrawal

```
POST /withdraw/recover/<withdrawal_id>
```

---

## Running the Project

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/User-Payout-Management-System.git
```

### 2. Navigate to project

```bash
cd User-Payout-Management-System
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Flask API

```bash
python api.py
```

Or run sample execution

```bash
python app.py
```

---

## Assumptions

- Data is stored in an in-memory database.
- Advance payout is fixed at **10%**.
- Final payout is processed only once.
- Wallet balance cannot become negative.
- Users can withdraw only once every 24 hours.
- Failed or rejected withdrawals are refundable only once.

---

## Future Improvements

- Replace in-memory storage with PostgreSQL or MySQL
- Add authentication and authorization
- Swagger/OpenAPI documentation
- Docker support
- Unit tests
- Repository pattern
- Transaction management
- Logging and monitoring

---

## Author

**Jiya**

Backend Developer | Python | Flask | REST APIs
