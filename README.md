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

### 5. `POST /admin/ingredients/tag`

**Description:** (Admin only) Submit an ingredient's risk factor components for tagging in the risk matrix.

**Request Body:**

```json
{
  "ingredient": "peanut oil",
  "base_match": 1.0,
  "severity_weight": 0.9,
  "dosage_factor": 0.4,
  "processing_adjustment": 0.5
}
```

**Response:**

```json
{
  "message": "Ingredient tagged successfully"
}
```

---

## ⚙️ Risk Score Formula

```
Final Score = BaseMatch × SeverityWeight × DosageFactor × ProcessingAdjustment
```

---

## 📚 Common Allergens (used when profile is incomplete)

* Peanuts
* Tree nuts
* Milk
* Eggs
* Wheat
* Soy
* Fish
* Shellfish
* Sesame
* Gluten
* Sulfites
* Mustard
* Celery
* Lupin

---

## 🔐 Future Additions (Deferred)

* Auth and session management
* Admin dashboard (React/Next.js)
* Allergy tracking & history
* Multilingual summaries
* Meal planner

---

## 🛠️ Tech Stack

* **FastAPI** (Backend API)
* **Uvicorn** (ASGI server)
* **Pydantic** (Data validation)
* **OpenAI/GPT / Mixtral** (LLM-based summaries)
* **Google ML Kit** (OCR - client side)
