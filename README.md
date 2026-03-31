# TaskFlow - Flodo Assignment

A robust, full-stack task management application built with Flutter and Python (FastAPI).

## Project Scope
* **Track Chosen:** Track A (The Full-Stack Builder)
* **Stretch Goal Chosen:** #3 (Persistent Drag-and-Drop Priority)

## Features
* **Full CRUD & SQLite Persistence:** Create, Read, Update, and Delete tasks.
* **Persistent Priority (Stretch Goal):** Drag and drop tasks in the UI to assign a permanent `#` priority rank. Rearranging or deleting tasks automatically updates the index sequence in the backend database.
* **Task Dependency System:** Tasks can be "Blocked By" other tasks. Blocked tasks are visually greyed out and the backend prevents users from marking them "In Progress" or "Done" until the blocker is complete.
* **Draft Recovery:** Unsaved form text is persisted locally. If you close the creation screen accidentally, your progress is restored via `SharedPreferences`.
* **Latency Simulation:** All backend write operations simulate a 2-second delay. The UI handles this gracefully with disabled buttons and progress indicators.
* **Search & Filter:** Instantly search by title and filter by status tags.

## Folder Structure
```bash
TaskFlow/
├── backend/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── frontend/
│   ├── lib/
│   │   ├── models/
│   │   ├── services/
│   │   └── screens/
│   └── pubspec.yaml
│
└── README.md
```

## Setup Instructions

### 1. Backend (Python/FastAPI)
1. Navigate to the backend folder: `cd backend`
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install fastapi uvicorn sqlalchemy pydantic`
5. Run the server: `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`

### 2. Frontend (Flutter)
1. Navigate to the frontend folder: `cd frontend`
2. Get packages: `flutter pub get`
3. *Important Network Note:* If running on a physical Android device via USB, run `adb reverse tcp:8000 tcp:8000` in your terminal to tunnel the connection to localhost. If using an Android Emulator, update the `baseUrl` in `lib/services/api_service.dart` to `10.0.2.2`.
4. Run the app: `flutter run`

## AI Usage Report
As encouraged in the guidelines, I utilized ChatGPT and Gemini to accelerate development:
* **Helpful Prompts:** I used AI to quickly generate the boilerplate for the SQLAlchemy models and Pydantic schemas, and to help structure the `ReorderableListView.builder` in Flutter.
* **Hallucinations & Fixes:** When implementing the batch API update for the drag-and-drop stretch goal, the AI initially suggested a loop that queried the database *N* times (once for every task moved). I recognized this was highly inefficient for scaling, so I refactored the Python logic myself to fetch all affected tasks in a single query and update them via an *O(1)* dictionary map lookup before committing the transaction.