from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import pathlib

from app.graph import travel_graph
from app.utils.export_pdf import export_to_pdf
from app.utils.export_docx import export_to_docx

# -----------------------------
# App initialization
# -----------------------------
app = FastAPI(title="Agentic AI Travel Planner")

BASE_DIR = pathlib.Path(__file__).parent

# Serve static files (UI)
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

# -----------------------------
# In-memory storage (latest plan)
# -----------------------------
LATEST_ITINERARY = {"text": ""}

# -----------------------------
# Request model
# -----------------------------
class TravelRequest(BaseModel):
    destination: str
    days: int
    people: int = 1
    budget: str = "budget"            # budget | mid | luxury
    travel_style: str = "solo"

# -----------------------------
# UI Home Page
# -----------------------------
@app.get("/", response_class=HTMLResponse)
def home():
    html_path = BASE_DIR / "static" / "index.html"
    return html_path.read_text(encoding="utf-8")

# -----------------------------
# MAIN AGENTIC ENDPOINT
# -----------------------------
@app.post("/plan-trip")
def plan_trip(req: TravelRequest):

    # Build natural language query for planner agent
    query = (
        f"Plan a {req.days}-day {req.budget} trip to {req.destination} "
        f"for {req.people} traveler(s)"
    )

    # 🔥 STEP 4B: Pass structured data into graph
    result = travel_graph.invoke({
        "query": query,
        "days": req.days,
        "people": req.people,
        "budget_type": req.budget
    })

    # SAFELY extract final output
    final_text = (
        result.get("final_output")
        or result.get("final_itinerary")
        or result.get("itinerary")
        or ""
    )

    if not final_text:
        raise ValueError(
            f"Graph returned no final output. Keys: {list(result.keys())}"
        )

    # Store latest itinerary for export
    LATEST_ITINERARY["text"] = final_text

    return {
        "destination": req.destination,
        "days": req.days,
        "people": req.people,
        "budget_type": req.budget,
        "itinerary": final_text
    }

# -----------------------------
# EXPORT AS PDF
# -----------------------------
@app.get("/export/pdf")
def export_pdf():
    if not LATEST_ITINERARY["text"]:
        return {"error": "No itinerary available. Generate a trip first."}

    filename = export_to_pdf(LATEST_ITINERARY["text"])

    return FileResponse(
        filename,
        media_type="application/pdf",
        filename=filename
    )

# -----------------------------
# EXPORT AS DOCX
# -----------------------------
@app.get("/export/docx")
def export_docx():
    if not LATEST_ITINERARY["text"]:
        return {"error": "No itinerary available. Generate a trip first."}

    filename = export_to_docx(LATEST_ITINERARY["text"])

    return FileResponse(
        filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename
    )
