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

#### POST /api/admin/signin
- Description: Authenticate admin and return JWT.
- Body (JSON): `{ username, password }`
- Response 200: same as signup response.

#### GET /api/admin/profile
- Auth: required
- Description: Get current admin profile.
- Response 200: `AdminOut` `{ id, username, email, phone, role, organization_id, created_at }`

#### PUT /api/admin/profile
- Auth: required
- Description: Update profile for current admin.
- Body (JSON): any updatable fields from `AdminUpdate` (e.g., `email`, `phone`, etc.).
- Response 200: Updated `AdminOut`.

#### GET /api/admin/list
- Auth: required (roles: Owner, Manager)
- Query: `skip` (int, default 0), `limit` (int, default 100)
- Description: List all admins.
- Response 200: `AdminOut[]`

#### GET /api/admin/{admin_id}
- Auth: required (roles: Owner, Manager)
- Description: Get admin by id.
- Response 200: `AdminOut`

### Vehicle Owner Wallet (Admin Tools)

#### POST /api/admin/search-vehicle-owner
- Auth: required
- Description: Lookup vehicle owner by primary phone number.
- Body (JSON): `{ primary_number: string }`
- Response 200: `VehicleOwnerInfoResponse` (owner profile + wallet balance)

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

### Order Operations (Admin Views & Controls)

#### GET /api/orders/admin/{order_id}
- Auth: required
- Description: Full order details for admin, including vendor, assignments, driver/car, vehicle owner, end records, profits.
- Response 200: `AdminOrderDetailResponse`

#### GET /api/admin/orders
- Auth: required
- Query (optional):
  - `vendor_id` (UUID), `trip_status` (string), `source` (NEW_ORDERS|HOURLY_RENTAL),
  - `start_date`, `end_date` (ISO8601)
- Description: List orders with filters.
- Response 200: `Order[]`

#### PATCH /api/admin/orders/{order_id}/cancel
- Auth: required
- Form (optional): `reason` (string)
- Description: Force-cancel an order. Sets `trip_status=CANCELLED`, `cancelled_by=ADMIN`.
- Response 200: `{ order_id, trip_status, cancelled_by, reason }`

### Vendor Transfer Requests (Admin Moderation)

#### GET /api/admin/transfers/pending
- Auth: required
- Query: `skip` (int, default 0), `limit` (int, default 100)
- Description: List pending vendor transfer requests.
- Response 200: `TransferHistoryOut` `{ transactions: TransferTransactionOut[], total_count }`

#### POST /api/admin/transfers/{transaction_id}/process
- Auth: required
- Description: Approve or reject a pending transfer request.
- Body (JSON) `AdminTransferAction`:
  - `action` (enum: APPROVE | REJECT)
  - `admin_notes` (string, optional)
- Response 200: `TransferTransactionOut`

#### GET /api/admin/transfers/{transaction_id}
- Auth: required
- Description: Get details of a specific transfer transaction.
- Response 200: `TransferTransactionOut`

#### GET /api/admin/vendors/{vendor_id}/balance
- Auth: required
- Description: Get wallet and bank balance for a vendor.
- Response 200: `VendorBalanceOut` `{ vendor_id, wallet_balance, bank_balance, total_balance }`

### Users Management (Drivers, Vehicle Owners, Vendors)

#### GET /api/admin/drivers
- Auth: required
- Query (optional): `vehicle_owner_id` (UUID), `status_filter` (ONLINE|OFFLINE|DRIVING|BLOCKED|PROCESSING)
- Description: List drivers with optional filters.
- Response 200: `CarDriver[]`

#### PATCH /api/admin/drivers/{driver_id}/status
- Auth: required
- Form: `new_status` (ONLINE|OFFLINE|DRIVING|BLOCKED|PROCESSING)
- Description: Admin override to set driver status.
- Response 200: `{ driver_id, new_status }`

#### PATCH /api/admin/drivers/{driver_id}/document-status
- Auth: required
- Form: `status_value` (PENDING|APPROVED|REJECTED)
- Description: Update driver licence document status.
- Response 200: `{ driver_id, licence_status }`

#### GET /api/admin/vehicle-owners
- Auth: required
- Query (optional): `mobile` (string), `city` (string)
- Description: List vehicle owners with filters.
- Response 200: `VehicleOwnerDetails[]`

#### PATCH /api/admin/vehicle-owners/{owner_id}/document-status
- Auth: required
- Form: `status_value` (PENDING|APPROVED|REJECTED)
- Description: Update vehicle owner Aadhar document status.
- Response 200: `{ vehicle_owner_id, aadhar_status }`

#### GET /api/admin/vendors
- Auth: required
- Query (optional): `mobile` (string), `city` (string)
- Description: List vendors with filters.
- Response 200: `VendorDetails[]`

#### PATCH /api/admin/vendors/{vendor_id}/document-status
- Auth: required
- Form: `status_value` (PENDING|APPROVED|REJECTED)
- Description: Update vendor Aadhar document status.
- Response 200: `{ vendor_id, aadhar_status }`

### Wallets & Transactions (Admin Views)

#### GET /api/admin/vehicle-owners/{owner_id}/wallet/ledger
- Auth: required
- Description: View vehicle owner wallet ledger.
- Response 200: `WalletLedger[]`

#### GET /api/admin/vendors/{vendor_id}/wallet/ledger
- Auth: required
- Description: View vendor wallet ledger.
- Response 200: `VendorWalletLedger[]`

#### GET /api/admin/admin-wallet/ledger
- Auth: required
- Description: View current admin wallet ledger.
- Response 200: `AdminWalletLedger[]`

#### GET /api/admin/admin-wallet/balance
- Auth: required
- Description: View current admin wallet balance.
- Response 200: `{ admin_id, current_balance }`

#### GET /api/admin/razorpay-transactions
- Auth: required
- Query (optional): `status_filter` (created|authorized|captured|failed|refunded), `owner_id` (UUID)
- Description: List Razorpay transactions.
- Response 200: `RazorpayTransaction[]`

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


