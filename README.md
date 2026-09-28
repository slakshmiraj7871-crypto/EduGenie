# 🎓 EduGenie: Google Gemini Powered Learning Assistant

[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://python.org)
[![Google Gemini](https://img.shields.io/badge/AI-Google%20Gemini-8E75C2?logo=google&logoColor=white)](https://aistudio.google.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**EduGenie** is a lightweight, full-stack AI-powered educational assistant that simplifies learning through modern Generative AI. Designed for students, educators, and lifelong learners of all academic levels, EduGenie enables users to:
1. **Academic Q&A**: Ask any homework or scientific question and receive smart, concise answers.
2. **Concept Explanation**: Demystify complex theories (e.g., Pythagoras Theorem, Black Holes) with intuitive everyday analogies and plain-language pedagogy.
3. **Interactive 3-Question MCQ Quiz**: Automatically generate three 4-option multiple-choice questions from any topic or passage, with real-time feedback, incorrect-answer corrections, and running score metrics.
4. **Passage Summarizer**: Condense lengthy articles and study guides into structured, high-yield revision summaries.
5. **Personalized Learning Paths**: Build structured, milestone-driven roadmaps spanning beginner to advanced levels with curated resources (books, videos, platforms).

---

## 🏗️ Project Architecture

```
EduGenie.AI/
├── .env                      # Local environment configuration (GEMINI_API_KEY)
├── .env.example              # Template environment configuration
├── .gitignore                # Git ignore rules for Python, cache, and env files
├── requirements.txt          # Python dependencies
├── main.py                   # FastAPI backend server & REST API endpoints
├── gemini_client.py          # Unified Google GenAI client with resilient error handling
├── qna.py                    # Academic Question Answering logic
├── explanation_module.py     # Dual-mode concept explanation (LaMini-Flan-T5 / Gemini)
├── quiz_module.py            # Quiz generator with clean_json_block & schema validation
├── summary_module.py         # Educational passage summarizer
├── learning_path.py          # Structured learning roadmap generator
├── test_app.py               # Automated pytest & FastAPI test suite
├── templates/
│   └── index.html            # Responsive Jinja2 frontend template
├── static/
│   ├── style.css             # Modern educational stylesheet & quiz UI styles
│   └── script.js             # Interactive client-side controller & MCQ score engine
└── .vscode/
    ├── launch.json           # VS Code Run/Debug configurations
    └── settings.json         # VS Code workspace settings & test discovery
```

---

## ⚡ Quick Start: VS Code Setup & Running

### Step 1: Open the Project in VS Code
1. Open **Visual Studio Code**.
2. Click **File** > **Open Folder...** (or press `Ctrl + K, Ctrl + O`).
3. Select the `EduGenie.AI` folder:
   ```
   c:\Users\ELCOT\Documents\EduGenie.AI
   ```

---

### Step 2: Open Terminal & (Optional) Create Virtual Environment
Open the built-in terminal in VS Code (`Ctrl + ` ` ` or **Terminal** > **New Terminal**):

```powershell
# 1. (Optional) Create a virtual environment
python -m venv venv

# 2. Activate the virtual environment
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
# On Windows Command Prompt (CMD):
.\venv\Scripts\activate.bat
# On macOS / Linux:
source venv/bin/activate
```

---

### Step 3: Install Dependencies
Run:
```bash
python -m pip install -r requirements.txt
```

---

### Step 4: Configure Your Gemini API Key
EduGenie uses the official Google Gemini API for cloud intelligence.

1. Get a **free** Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Open the `.env` file in the root directory (or copy `.env.example` to `.env`):
   ```ini
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-flash
   USE_LOCAL_LAMINI=false
   ```
3. Save the file (`Ctrl + S`).

> 💡 **Notice**: If you run the app before adding your API key, EduGenie will still start smoothly, display a badge in the header, and provide helpful guidance whenever an AI feature is invoked.

---

### Step 5: Run EduGenie

#### Method A: Terminal (Recommended)
Run the following command in your terminal:
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

#### Method B: VS Code 1-Click Debugger
1. Press `F5` or switch to the **Run & Debug** tab on the left sidebar (`Ctrl + Shift + D`).
2. Select **"Python: EduGenie FastAPI Server"** from the dropdown.
3. Click the green **Play (▶)** button.

---

### Step 6: Open the Application
- **Interactive Web App**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger API Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check Endpoint**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🧪 Testing EduGenie

### Automated Tests with Pytest
EduGenie includes a complete automated test suite verifying routing, health status, request parsing, empty-input validation, JSON cleaning, and AI responses:

```bash
python -m pytest test_app.py -v
```

Expected result:
```
test_app.py::test_health_endpoint PASSED                    [ 14%]
test_app.py::test_home_page PASSED                          [ 28%]
test_app.py::test_request_model_parameter_resolution PASSED [ 42%]
test_app.py::test_empty_input_validation PASSED             [ 57%]
test_app.py::test_quiz_clean_json_block PASSED              [ 71%]
test_app.py::test_endpoint_mock_execution PASSED            [ 85%]
test_app.py::test_quiz_mock_execution PASSED                [100%]
======================== 7 passed in 0.85s =========================
```

---

## 🧭 Exploring EduGenie: 5 Core Scenarios

| Scenario | Mode Selected | Example Input | Expected Output |
| :--- | :--- | :--- | :--- |
| **1. Academic Q&A** | `Academic Q&A` | *"Which is the largest ocean?"* | Direct answer (Pacific Ocean), physical dimensions, facts, and summary. |
| **2. Concept Simplification** | `Concept Explanation` | *"The Pythagoras Theorem"* | Everyday analogy (ladder against a wall), simple mathematical breakdown, and takeaway. |
| **3. Interactive Quiz** | `Generate Quiz` | *"Renewable vs Non-Renewable Energy"* | 3 interactive MCQ cards with 4 options each, real-time score tracking, instant green/red answer reveal, and pedagogical explanations. |
| **4. Quick Revision** | `Passage Summarizer` | *Paste textbook passage* | 3-part structured revision: Concept Overview, Key High-Yield Points, and Exam Takeaway. |
| **5. Learning Roadmap** | `Learning Path` | *"SQL for Data Science"* | Step-by-step roadmap: Stage 1 (Foundations), Stage 2 (Intermediate), Stage 3 (Advanced), with timelines & curated resources. |

---

## 📡 REST API Reference

| Method | Endpoint | Description | Sample Request Body |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | Web frontend UI | None |
| `GET` | `/health` | System & API configuration health status | None |
| `POST` | `/qa` | Answer student questions | `{"prompt": "Which is the largest ocean?"}` |
| `POST` | `/explain` | Simplified concept explanation | `{"prompt": "The Pythagoras Theorem"}` |
| `POST` | `/quiz` | 3 MCQs in structured JSON format | `{"prompt": "Renewable Energy"}` |
| `POST` | `/summarize` | Educational passage summarizer | `{"prompt": "Textbook text..."}` |
| `POST` | `/learn/recommendations` | Structured learning roadmap | `{"prompt": "SQL for Data Science"}` |

---

## 🛠️ Advanced: Local LaMini-Flan-T5-783M Setup (Optional)
If you wish to run the local `MBZUAI/LaMini-Flan-T5-783M` model instead of cloud inference for concept explanations:
1. Install PyTorch and Hugging Face Transformers:
   ```bash
   pip install torch transformers sentencepiece
   ```
2. In your `.env` file, set:
   ```ini
   USE_LOCAL_LAMINI=true
   ```
3. When `/explain` is called, EduGenie will automatically load `MBZUAI/LaMini-Flan-T5-783M` using CPU/GPU pipeline. If unavailable, it seamlessly falls back to Gemini.
