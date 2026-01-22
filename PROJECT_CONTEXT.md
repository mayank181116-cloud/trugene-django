# PROJECT CONTEXT — TRUGENE (Django)

## 1. Project Overview

**Project Name:** Trugene
**Type:** Healthcare / Diagnostic Booking Platform
**Goal:** Build a professional, scalable, mobile‑friendly diagnostic test & health package booking system with OTP-based verification and future-ready integrations (SMS, payment, admin automation).

The system is designed step‑by‑step with a **production mindset**, even while running locally in development.

---

## 2. Current Tech Stack

* **Backend:** Django 6.x
* **Database:** SQLite (temporary, will migrate later)
* **Frontend:** Django Templates (mobile‑first, simple inline styles)
* **OTP System:** Custom OTP logic (DB‑based)
* **SMS Provider (future):** Fast2SMS (DLT pending)
* **Environment Management:** `.env` file for secrets
* **OS:** Windows (local development)

---

## 3. Apps Structure (Why Multiple Apps)

We intentionally split responsibilities to keep the system **clean, scalable, and professional**.

### 📦 `packages` app (CORE USER FLOW)

Handles everything related to **public users**:

* Health package listing
* Package booking
* OTP verification
* OTP resend logic
* Booking success flow

This app represents **real customer interaction**.

---

### 🧪 `tests` app (SUPPORT / DATA)

Handles **supporting models**:

* `MobileOTP` model
* (Earlier experiments with HealthPackage & Booking — now stabilized)

This separation avoids bloated apps and keeps OTP logic reusable later.

---

### 🛠 `services` app (FUTURE USE)

Reserved for:

* SMS services
* Payment gateways
* Email services
* External APIs

Currently minimal, but kept intentionally for **enterprise‑grade architecture**.

---

## 4. Database Models (Current Truth)

### `HealthPackage`

* name
* short_description
* tests_included
* price
* is_active

### `Booking`

* phone_number
* package (FK → HealthPackage)
* is_verified (future use)
* created_at

### `MobileOTP`

* mobile (phone number)
* otp (string)
* resend_count
* created_at

OTP records are **deleted after success** to prevent reuse.

---

## 5. User Flow (What Works Now)

1. User visits `/packages/`
2. Sees list of active health packages
3. Clicks **Book Now**
4. Enters mobile number
5. System:

   * Creates booking
   * Generates OTP
   * Saves OTP in DB
   * Prints OTP in terminal (DEV MODE)
6. User enters OTP on verify page
7. OTP validated against DB
8. User redirected to **Booking Success** page

---

## 6. OTP System (Current Decisions)

### Why Custom OTP?

* Full control
* No vendor lock‑in
* Easy to debug
* Enterprise‑ready

### Current Rules

* OTP stored in DB
* Latest OTP only
* Resend limit: **max 3 times**
* Expiry temporarily disabled (for stability)
* SMS sending temporarily optional

> OTP expiry & DLT will be reintroduced after system stabilizes.

---

## 7. Environment & Security

### `.env` Usage

* Secrets like `FAST2SMS_API_KEY`
* Loaded via `settings.py`
* Never hard‑coded in production

This prepares the project for **cloud deployment**.

---

## 8. What We Fixed Along the Way (Important Learnings)

* Template path mistakes (`temlates` vs `templates`)
* App import errors (`accounts` removed)
* Admin import conflicts
* OTP field name mismatch (`mobile` vs `phone_number`)
* Duplicate OTP creation bugs
* Session handling mistakes
* Terminal vs Django shell confusion

These fixes shaped the **current clean structure**.

---

## 9. What We Are NOT Doing Yet (Intentionally)

* ❌ Production deployment
* ❌ DLT registration
* ❌ Payment gateway
* ❌ User authentication
* ❌ API versioning

Reason: **Stability first, scale later**.

---

## 10. Next Planned Professional Steps

1. OTP expiry (configurable)
2. Failed OTP attempt limit
3. Booking verification flag update
4. Admin dashboard automation
5. Payment integration
6. SMS DLT compliance
7. REST API (DRF)
8. React / Mobile frontend
9. Cloud deployment (Render / AWS)

---

## 11. How To Resume Work In Next Chat

Say:

> "Continue Trugene from PROJECT_CONTEXT.md"

This document represents the **single source of truth** for the project.

---

## 12. Design Philosophy

* Simple > Complex
* Stable > Fancy
* Scalable > Quick hacks
* Production mindset from Day 1

---

### Status: ✅ STABLE DEVELOPMENT BASE

Ready to evolve into a **high‑class professional healthcare platform** 🚀
