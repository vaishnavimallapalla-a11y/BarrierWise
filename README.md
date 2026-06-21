# BarrierWise

A full-stack web app for skincare and haircare product recommendations based on quizzes.

## Setup Backend

1. Navigate to the `backend` directory.
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment:
   - Windows: `venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Seed the database: `python seed.py`
6. Run the server: `uvicorn main:app --reload --port 8000`

The API will be available at `http://localhost:8000`.

## Setup Frontend

1. Navigate to the `frontend` directory.
2. Install dependencies: `npm install`
3. Install additional dependencies: `npm install react-router-dom lucide-react`
4. Run the development server: `npm run dev`

The app will be available at `http://localhost:5173`.
