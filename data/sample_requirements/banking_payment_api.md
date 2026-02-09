# Project: Payment Processing API

## Overview
Build a REST API for processing customer payments within our banking platform.

## Requirements

### Authentication
- Users should be authenticated before accessing any endpoint
- Use secure authentication method
- Support role-based access control (admin, teller, customer)

### Payment Processing
- Accept payment requests with amount, sender, receiver, and currency
- Validate payment details before processing
- Support multiple currencies (USD, EUR, GBP)
- Generate unique transaction IDs
- Store transaction history

### Notifications
- Send confirmation after successful payment
- Alert on failed transactions
- Provide real-time transaction status

### API
- RESTful endpoints
- JSON request/response format
- Proper error handling with meaningful messages
- API versioning

### Non-Functional
- Response time under 200ms
- Handle 500 concurrent transactions
- 99.9% uptime SLA
- Comprehensive audit logging
