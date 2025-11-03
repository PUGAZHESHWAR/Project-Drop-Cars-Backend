## Admin App API (Consolidated)

This document consolidates all backend APIs required by the Admin app. Every admin-protected endpoint requires a valid JWT in the `Authorization` header.

- Authentication scheme: Bearer JWT
- Header for protected routes: `Authorization: Bearer <token>`
- Token issuance: via `/api/admin/signin` or `/api/admin/signup`

### Authentication

- Secret/Alg (server): HS256
- Token payload: `{ "sub": "<admin_id>", "exp": <expiry> }`
- Token verification middleware: `get_current_admin`

#### POST /api/admin/signup
- Description: Create an admin and return a JWT.
- Body (JSON):
  - `username` (string, required)
  - `password` (string, required)
  - `role` (string, one of: Owner, Manager, Staff)
  - `email` (string)
  - `phone` (string)
- Response 201 (JSON):
  - `access_token` (string)
  - `token_type` = "bearer"
  - `admin` (object): `{ id, username, email, phone, role, organization_id, created_at }`

Request
```json
{
  "username": "admin1",
  "password": "secret",
  "role": "Owner",
  "email": "admin@example.com",
  "phone": "+911234567890"
}
```

Response 201
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "admin": {
    "id": "2d8f4d9e-...",
    "username": "admin1",
    "email": "admin@example.com",
    "phone": "+911234567890",
    "role": "Owner",
    "organization_id": null,
    "created_at": "2025-11-03T08:40:00Z"
  }
}
```

#### POST /api/admin/signin
- Description: Authenticate admin and return JWT.
- Body (JSON): `{ username, password }`
- Response 200: same as signup response.

Request
```json
{ "username": "admin1", "password": "secret" }
```

Response 200
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "admin": { "id": "2d8f4d9e-...", "username": "admin1", "email": "admin@example.com", "phone": "+911234567890", "role": "Owner", "organization_id": null, "created_at": "2025-11-03T08:40:00Z" }
}
```

#### GET /api/admin/profile
- Auth: required
- Description: Get current admin profile.
- Response 200: `AdminOut` `{ id, username, email, phone, role, organization_id, created_at }`

Response 200
```json
{ "id": "2d8f4d9e-...", "username": "admin1", "email": "admin@example.com", "phone": "+911234567890", "role": "Owner", "organization_id": null, "created_at": "2025-11-03T08:40:00Z" }
```

#### PUT /api/admin/profile
- Auth: required
- Description: Update profile for current admin.
- Body (JSON): any updatable fields from `AdminUpdate` (e.g., `email`, `phone`, etc.).
- Response 200: Updated `AdminOut`.

Request
```json
{ "email": "new-admin@example.com", "phone": "+911112223334" }
```

Response 200
```json
{ "id": "2d8f4d9e-...", "username": "admin1", "email": "new-admin@example.com", "phone": "+911112223334", "role": "Owner", "organization_id": null, "created_at": "2025-11-03T08:40:00Z" }
```

#### GET /api/admin/list
- Auth: required (roles: Owner, Manager)
- Query: `skip` (int, default 0), `limit` (int, default 100)
- Description: List all admins.
- Response 200: `AdminOut[]`

Response 200
```json
[
  { "id": "2d8f4d9e-...", "username": "admin1", "email": "admin1@example.com", "phone": "+911234567890", "role": "Owner", "organization_id": null, "created_at": "2025-10-01T10:00:00Z" },
  { "id": "4a2f8b77-...", "username": "manager1", "email": "mgr@example.com", "phone": "+919998887776", "role": "Manager", "organization_id": null, "created_at": "2025-10-10T12:00:00Z" }
]
```

#### GET /api/admin/{admin_id}
- Auth: required (roles: Owner, Manager)
- Description: Get admin by id.
- Response 200: `AdminOut`

Response 200
```json
{ "id": "4a2f8b77-...", "username": "manager1", "email": "mgr@example.com", "phone": "+919998887776", "role": "Manager", "organization_id": null, "created_at": "2025-10-10T12:00:00Z" }
```

### Vehicle Owner Wallet (Admin Tools)

#### POST /api/admin/search-vehicle-owner
- Auth: required
- Description: Lookup vehicle owner by primary phone number.
- Body (JSON): `{ primary_number: string }`
- Response 200: `VehicleOwnerInfoResponse` (owner profile + wallet balance)

Request
```json
{ "primary_number": "+919876543210" }
```

Response 200
```json
{
  "vehicle_owner_id": "e0c2c3a9-...",
  "full_name": "John Doe",
  "primary_number": "+919876543210",
  "secondary_number": "+919112233445",
  "wallet_balance": 1500,
  "aadhar_number": "1234-5678-9012",
  "aadhar_front_img": "https://.../aadhar.jpg",
  "address": "Street 1",
  "city": "Chennai",
  "pincode": "600001"
}
```

#### POST /api/admin/add-money-to-vehicle-owner
- Auth: required
- Content-Type: multipart/form-data
- Description: Credit a vehicle owner's wallet and record admin transaction (optional proof upload).
- Form fields:
  - `vehicle_owner_id` (string, UUID, required)
  - `transaction_value` (int, paise, required)
  - `notes` (string, optional)
  - `reference_value` (string, optional)
  - `transaction_img` (file .jpg/.jpeg/.png/.pdf, optional)
- Response 201: `{ transaction_id: UUID }`

Request (multipart/form-data)
```
vehicle_owner_id=e0c2c3a9-...
transaction_value=50000
notes=Manual credit
reference_value=UTR123
transaction_img=<file>
```

Response 201
```json
{ "transaction_id": "b1b2c3d4-..." }
```

### Order Operations (Admin Views & Controls)

#### GET /api/orders/admin/{order_id}
- Auth: required
- Description: Full order details for admin, including vendor, assignments, driver/car, vehicle owner, end records, profits.
- Response 200: `AdminOrderDetailResponse`

Response 200 (truncated)
```json
{
  "order": {
    "id": 123,
    "source": "NEW_ORDERS",
    "trip_type": "ONEWAY",
    "vendor_id": "c7c9...",
    "customer_name": "Alice",
    "customer_number": "+91900...",
    "estimated_price": 4500,
    "vendor_price": 5200,
    "admin_profit": 120,
    "vendor_profit": 580
  },
  "assignments": [ { "id": 10, "assignment_status": "ASSIGNED" } ],
  "driver": { "id": "d1..", "full_name": "Driver 1", "primary_number": "+91988..." },
  "car": { "id": "car1..", "car_name": "Swift" },
  "vehicle_owner": { "id": "e0c2...", "full_name": "John Doe" },
  "end_records": []
}
```

#### GET /api/admin/orders
- Auth: required
- Query (optional):
  - `vendor_id` (UUID), `trip_status` (string), `source` (NEW_ORDERS|HOURLY_RENTAL),
  - `start_date`, `end_date` (ISO8601)
- Description: List orders with filters.
- Response 200: `Order[]`

Response 200 (example item)
```json
[
  {
    "id": 123,
    "source": "NEW_ORDERS",
    "source_order_id": 456,
    "vendor_id": "c7c9...",
    "trip_type": "ONEWAY",
    "car_type": "SEDAN",
    "pickup_drop_location": { "pickup": "Chennai", "drop": "Vellore" },
    "start_date_time": "2025-11-04T09:00:00Z",
    "customer_name": "Alice",
    "customer_number": "+91900...",
    "trip_status": "PENDING",
    "estimated_price": 4500,
    "vendor_price": 5200,
    "admin_profit": 120,
    "vendor_profit": 580,
    "created_at": "2025-11-03T08:50:00Z"
  }
]
```

#### PATCH /api/admin/orders/{order_id}/cancel
- Auth: required
- Form (optional): `reason` (string)
- Description: Force-cancel an order. Sets `trip_status=CANCELLED`, `cancelled_by=ADMIN`.
- Response 200: `{ order_id, trip_status, cancelled_by, reason }`

Request (form)
```
reason=Customer requested
```

Response 200
```json
{ "order_id": 123, "trip_status": "CANCELLED", "cancelled_by": "ADMIN", "reason": "Customer requested" }
```

### Vendor Transfer Requests (Admin Moderation)

#### GET /api/admin/transfers/pending
- Auth: required
- Query: `skip` (int, default 0), `limit` (int, default 100)
- Description: List pending vendor transfer requests.
- Response 200: `TransferHistoryOut` `{ transactions: TransferTransactionOut[], total_count }`

Response 200 (truncated)
```json
{
  "transactions": [
    { "id": "t1..", "vendor_id": "v1..", "requested_amount": 10000, "status": "PENDING", "created_at": "2025-11-01T10:00:00Z" }
  ],
  "total_count": 1
}
```

#### POST /api/admin/transfers/{transaction_id}/process
- Auth: required
- Description: Approve or reject a pending transfer request.
- Body (JSON) `AdminTransferAction`:
  - `action` (enum: APPROVE | REJECT)
  - `admin_notes` (string, optional)
- Response 200: `TransferTransactionOut`

Request
```json
{ "action": "APPROVE", "admin_notes": "Paid via IMPS" }
```

Response 200
```json
{ "id": "t1..", "vendor_id": "v1..", "requested_amount": 10000, "status": "APPROVED", "admin_notes": "Paid via IMPS", "updated_at": "2025-11-03T09:10:00Z" }
```

#### GET /api/admin/transfers/{transaction_id}
- Auth: required
- Description: Get details of a specific transfer transaction.
- Response 200: `TransferTransactionOut`

Response 200
```json
{ "id": "t1..", "vendor_id": "v1..", "requested_amount": 10000, "status": "PENDING", "created_at": "2025-11-01T10:00:00Z" }
```

#### GET /api/admin/vendors/{vendor_id}/balance
- Auth: required
- Description: Get wallet and bank balance for a vendor.
- Response 200: `VendorBalanceOut` `{ vendor_id, wallet_balance, bank_balance, total_balance }`

Response 200
```json
{ "vendor_id": "v1..", "wallet_balance": 50000, "bank_balance": 250000, "total_balance": 300000 }
```

### Users Management (Drivers, Vehicle Owners, Vendors)

#### GET /api/admin/drivers
- Auth: required
- Query (optional): `vehicle_owner_id` (UUID), `status_filter` (ONLINE|OFFLINE|DRIVING|BLOCKED|PROCESSING)
- Description: List drivers with optional filters.
- Response 200: `CarDriver[]`

Response 200 (example item)
```json
[
  {
    "id": "d1..",
    "vehicle_owner_id": "e0c2..",
    "full_name": "Driver 1",
    "primary_number": "+91988...",
    "secondary_number": "+91977...",
    "licence_number": "TN-XX-YYYYY",
    "licence_front_img": "https://...",
    "licence_front_status": "PENDING",
    "address": "Street 2",
    "city": "Chennai",
    "pincode": "600001",
    "driver_status": "OFFLINE",
    "created_at": "2025-11-02T07:00:00Z"
  }
]
```

#### PATCH /api/admin/drivers/{driver_id}/status
- Auth: required
- Form: `new_status` (ONLINE|OFFLINE|DRIVING|BLOCKED|PROCESSING)
- Description: Admin override to set driver status.
- Response 200: `{ driver_id, new_status }`

Request (form)
```
new_status=BLOCKED
```

Response 200
```json
{ "driver_id": "d1..", "new_status": "BLOCKED" }
```

#### PATCH /api/admin/drivers/{driver_id}/document-status
- Auth: required
- Form: `status_value` (PENDING|APPROVED|REJECTED)
- Description: Update driver licence document status.
- Response 200: `{ driver_id, licence_status }`

Request (form)
```
status_value=APPROVED
```

Response 200
```json
{ "driver_id": "d1..", "licence_status": "APPROVED" }
```

#### GET /api/admin/vehicle-owners
- Auth: required
- Query (optional): `mobile` (string), `city` (string)
- Description: List vehicle owners with filters.
- Response 200: `VehicleOwnerDetails[]`

Response 200 (example item)
```json
[
  {
    "id": "det1..",
    "vehicle_owner_id": "e0c2..",
    "full_name": "John Doe",
    "primary_number": "+91987...",
    "secondary_number": "+91911...",
    "wallet_balance": 1500,
    "aadhar_number": "1234-5678-9012",
    "aadhar_front_img": "https://...",
    "aadhar_status": "PENDING",
    "address": "Street 1",
    "city": "Chennai",
    "pincode": "600001",
    "created_at": "2025-10-20T06:00:00Z"
  }
]
```

#### PATCH /api/admin/vehicle-owners/{owner_id}/document-status
- Auth: required
- Form: `status_value` (PENDING|APPROVED|REJECTED)
- Description: Update vehicle owner Aadhar document status.
- Response 200: `{ vehicle_owner_id, aadhar_status }`

Request (form)
```
status_value=REJECTED
```

Response 200
```json
{ "vehicle_owner_id": "e0c2..", "aadhar_status": "REJECTED" }
```

#### GET /api/admin/vendors
- Auth: required
- Query (optional): `mobile` (string), `city` (string)
- Description: List vendors with filters.
- Response 200: `VendorDetails[]`

Response 200 (example item)
```json
[
  {
    "id": "vd1..",
    "vendor_id": "v1..",
    "full_name": "Vendor One",
    "primary_number": "+91955...",
    "secondary_number": "+91944...",
    "wallet_balance": 10000,
    "bank_balance": 90000,
    "gpay_number": "+91955...",
    "aadhar_number": "4321-8765-2109",
    "aadhar_front_img": "https://...",
    "aadhar_status": "APPROVED",
    "address": "Vendor St",
    "city": "Chennai",
    "pincode": "600002",
    "created_at": "2025-10-15T05:00:00Z"
  }
]
```

#### PATCH /api/admin/vendors/{vendor_id}/document-status
- Auth: required
- Form: `status_value` (PENDING|APPROVED|REJECTED)
- Description: Update vendor Aadhar document status.
- Response 200: `{ vendor_id, aadhar_status }`

Request (form)
```
status_value=PENDING
```

Response 200
```json
{ "vendor_id": "v1..", "aadhar_status": "PENDING" }
```

### Wallets & Transactions (Admin Views)

#### GET /api/admin/vehicle-owners/{owner_id}/wallet/ledger
- Auth: required
- Description: View vehicle owner wallet ledger.
- Response 200: `WalletLedger[]`

Response 200 (example item)
```json
[
  {
    "id": "wl1..",
    "vehicle_owner_id": "e0c2..",
    "reference_id": "pay_123",
    "reference_type": "RAZORPAY_PAYMENT",
    "entry_type": "CREDIT",
    "amount": 500,
    "balance_before": 1000,
    "balance_after": 1500,
    "notes": "Topup",
    "created_at": "2025-11-03T08:30:00Z"
  }
]
```

#### GET /api/admin/vendors/{vendor_id}/wallet/ledger
- Auth: required
- Description: View vendor wallet ledger.
- Response 200: `VendorWalletLedger[]`

Response 200 (example item)
```json
[
  {
    "id": "vwl1..",
    "vendor_id": "v1..",
    "order_id": 123,
    "entry_type": "CREDIT",
    "amount": 580,
    "balance_before": 10000,
    "balance_after": 10580,
    "notes": "Trip 123 vendor profit",
    "created_at": "2025-11-03T08:55:00Z"
  }
]
```

#### GET /api/admin/admin-wallet/ledger
- Auth: required
- Description: View current admin wallet ledger.
- Response 200: `AdminWalletLedger[]`

Response 200 (example item)
```json
[
  {
    "id": "awl1..",
    "admin_id": "2d8f4d9e-...",
    "order_id": 123,
    "entry_type": "CREDIT",
    "amount": 120,
    "created_at": "2025-11-03T08:56:00Z"
  }
]
```

#### GET /api/admin/admin-wallet/balance
- Auth: required
- Description: View current admin wallet balance.
- Response 200: `{ admin_id, current_balance }`

Response 200
```json
{ "admin_id": "2d8f4d9e-...", "current_balance": 1200 }
```

#### GET /api/admin/razorpay-transactions
- Auth: required
- Query (optional): `status_filter` (created|authorized|captured|failed|refunded), `owner_id` (UUID)
- Description: List Razorpay transactions.
- Response 200: `RazorpayTransaction[]`

Response 200 (example item)
```json
[
  {
    "id": "rptx1..",
    "vehicle_owner_id": "e0c2..",
    "rp_order_id": "order_ABC",
    "rp_payment_id": "pay_123",
    "rp_signature": "sig_...",
    "amount": 50000,
    "currency": "INR",
    "status": "captured",
    "captured": true,
    "notes": null,
    "created_at": "2025-11-03T08:25:00Z",
    "updated_at": "2025-11-03T08:27:00Z"
  }
]
```

### General Orders (Optional for Admin Dashboards)

#### GET /api/orders/all
- Auth: not required (use cautiously; protect via gateway if needed)
- Description: List all orders (lightweight unified view).
- Response 200: `UnifiedOrder[]`

### Error Responses (common)

- 400: Validation error or business rule failure
- 401: Missing/invalid token, or subject not found
- 403: Insufficient permissions (role-based)
- 404: Resource not found
- 500: Internal server error

### Authentication Usage

Include the admin JWT in requests to protected endpoints:

```http
Authorization: Bearer <access_token>
```

Example curl for signin and fetching profile:

```bash
curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"admin1","password":"secret"}' \
  http://localhost:8000/api/admin/signin | jq -r .access_token

curl -s -H "Authorization: Bearer <token>" \
  http://localhost:8000/api/admin/profile
```

### Notes

- All admin-protected routes are validated by `get_current_admin`, which verifies JWT signature, expiry, and ensures the subject exists in DB.
- Roles are enforced explicitly where needed (e.g., listing/viewing admins).
- File uploads for admin transactions are uploaded to GCS under `admin_transactions/`.


