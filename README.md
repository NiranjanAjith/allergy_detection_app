# 🧪 Allergy Detection Backend API (FastAPI)

This is a proof-of-concept (PoC) FastAPI backend for the **Allergy Detection App**, which evaluates food safety based on user allergy profiles and scanned ingredient labels. The backend handles risk scoring, LLM-based summary generation, user profile management, and ingredient review.

---

## 📦 Setup Instructions

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the app**

   Run from the root of the project (above `app/` folder):

   ```bash
   python -m uvicorn app.main:app --reload
   ```

---

## 📱 API Endpoints

### 1. `GET /`

**Description:** Health check / Welcome endpoint

**Response:**

```json
{
  "message": "Allergy Detection API is running"
}
```

---

### 2. `POST /analyze`

**Description:** Analyze a list of scanned ingredients against the user’s allergy profile and generate a human-readable summary using LLM.

**Request Body:**

```json
{
  "ingredients": ["peanut oil", "wheat starch", "soy lecithin"],
  "profile": {
    "allergies": ["peanuts", "wheat"]
  }
}
```

> If `profile.allergies` is empty or omitted, the system will use a default list of 14 common allergens.

**Response:**

```json
{
  "risk_scores": [
    {
      "ingredient": "peanut oil",
      "score": 0.18
    },
    {
      "ingredient": "wheat starch",
      "score": 0.85
    }
  ],
  "summary": "This product contains peanut oil and wheat starch, which may pose a high risk based on your allergy profile. It is advised to avoid this item."
}
```

---

### 3. `GET /profile/{user_id}`

**Description:** Fetch a user’s saved allergy profile by ID

**Response:**

```json
{
  "user_id": "123",
  "allergies": ["peanuts", "gluten"]
}
```

---

### 4. `POST /profile`

**Description:** Create or update a user allergy profile

**Request Body:**

```json
{
  "user_id": "123",
  "allergies": ["peanuts", "gluten"]
}
```

**Response:**

```json
{
  "message": "Profile saved successfully"
}
```
---
