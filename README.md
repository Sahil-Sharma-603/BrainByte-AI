````markdown
# 🧠 BrainByte – AI Quiz App for Law Enforcement Aspirants

BrainByte is a **Python-based AI-powered quiz application** designed for individuals preparing
for law enforcement exams.

The platform generates AI-powered questions to help improve:

- 🧠 Working Memory  
- ✍️ Grammar & Language Skills  
- 🗺 Map Navigation  
- 🧩 Logical Reasoning  
- 📚 Exam-focused cognitive abilities  

---

# 🚀 Tech Stack

## 🔙 Backend
- Python  
- FastAPI  
- UV (Python package manager)  
- Clerk Backend API  

## ⚛️ Frontend
- React (Vite)  
- React Router v6  
- Clerk React SDK  

---

# 📦 Project Setup Guide

---

# 🔙 Backend Setup

### 1️⃣ Initialize UV

Inside your backend directory:

```bash
uv init .
````

---

### 2️⃣ Add Required Dependencies

```bash
uv add clerk-backend-api fastapi
```

To add any additional dependency:

```bash
uv add <dependency-name>
```

---

### 3️⃣ Run Backend Server

```bash
uv run server.py
```

---

### 🔢 Changing Number of Question Quotas

To modify the number of questions generated:

1. Open:

   * `model.py`
   * `db.py`
2. Locate the quota variable.
3. Update the number.
4. Restart backend server.

---

# ⚛️ Frontend Setup

### 1️⃣ Create Frontend Using Vite

From the project root:

```bash
npm create vite@latest frontend -- --template react
```

---

### 2️⃣ Install Dependencies

Navigate to frontend folder:

```bash
cd frontend
npm install
npm install react-router-dom@6 @clerk/clerk-react
```

---

### 3️⃣ Run Frontend

```bash
npm run dev
```


---

# 🧠 How BrainByte Works

1. User signs in using Clerk Authentication.
2. User selects quiz category.
3. Backend generates AI-based questions.
4. Questions are served via FastAPI.
5. Frontend displays quiz dynamically.
6. Results help track preparation level.

---

# 🎯 Target Users

* Law enforcement exam aspirants
* Competitive exam candidates
* Individuals improving cognitive performance

---

# 🔮 Future Improvements

* Performance analytics dashboard
* Timed mock tests
* Difficulty levels
* Admin control panel
* Deployment (Vercel / Railway / Render)

---

# 👨‍💻 Author

**Sahil Sharma**

---

