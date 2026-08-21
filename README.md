# ✈️ Agentic AI Travel Planner

An agentic AI travel-planning application that transforms a user's trip requirements into a structured, day-wise itinerary with attractions, budget analysis, and downloadable travel plans.

The project explores how a travel-planning problem can be decomposed into smaller tasks and handled by specialized AI agents orchestrated through **LangGraph**.

---

## 🎯 Problem

Planning a trip involves several connected decisions:

* Understanding what the traveler actually wants
* Finding suitable attractions and activities
* Organizing them into a realistic day-wise schedule
* Estimating the cost of the trip
* Adjusting the plan based on budget and travel intensity

A single LLM prompt can generate an itinerary, but it becomes harder to control and reason about when all of these responsibilities are handled together.

I built this project to explore a different approach: **decomposing travel planning into specialized agents, where each agent is responsible for one part of the planning process.**

---

## 💡 What I Wanted the Product to Do

The goal was to make the planning experience simple from the user's perspective.

The user provides:

* Destination
* Number of days
* Number of travelers
* Budget type
* Travel style

The system then handles the planning workflow and produces a structured itinerary.

The complexity of the multi-agent workflow stays behind the interface so that the user can focus on the final travel plan rather than how it was generated.

---

## 🧠 Agentic Approach

Instead of using one LLM call for the entire task, the application divides the problem into specialized agents.

```text
User Trip Request
       ↓
Planner Agent
       ↓
Attraction Agent
       ↓
Itinerary Agent
       ↓
Budget Agent
       ↓
Critic Agent
       ↓
Final Travel Plan
```

### 1. Planner Agent

The Planner Agent interprets the user's request and extracts important trip requirements:

* Destination
* Number of days
* Budget
* Travel style

Its output becomes the initial planning context for the rest of the workflow.

---

### 2. Attraction Agent

The Attraction Agent uses the trip plan to suggest relevant attractions and activities.

This separates the **"what should I do?"** problem from the later **"how should I schedule it?"** problem.

---

### 3. Itinerary Agent

The Itinerary Agent converts the suggested attractions into a day-wise itinerary.

It is instructed to:

* Avoid overloading individual days
* Balance travel and rest
* Organize activities into morning, afternoon, and evening

---

### 4. Budget Agent

The Budget Agent evaluates the itinerary from a cost perspective.

The application uses deterministic expense estimates for three budget categories:

| Budget Type |   Stay |   Food | Local Travel | Activities |
| ----------- | -----: | -----: | -----------: | ---------: |
| Budget      | ₹1,500 |   ₹800 |         ₹500 |       ₹700 |
| Mid         | ₹3,000 | ₹1,500 |         ₹800 |     ₹1,200 |
| Luxury      | ₹6,000 | ₹3,000 |       ₹1,500 |     ₹2,500 |

These values provide a predictable baseline rather than asking the LLM to invent every cost.

The agent then uses the itinerary and these estimates to review whether the planned trip is realistic and suggest potential savings.

---

### 5. Critic Agent

The Critic Agent is the final stage of the workflow.

It receives:

* Generated itinerary
* Budget review
* Daily budget estimate
* Number of days
* Number of travelers

It then produces the final structured travel plan, including:

* Morning activities
* Afternoon activities
* Evening activities
* Daily cost breakdown
* Per-person total
* Total trip cost

The application also uses deterministic calculations for the final multiplication of:

```text
Per-person daily cost × Number of days × Number of travelers
```

This keeps basic arithmetic outside the LLM.

---

## 🏗️ Architecture

The agents are orchestrated using **LangGraph StateGraph**.

Each agent receives and updates a shared `TravelState`.

```text
                    ┌─────────────────┐
                    │   User Request  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Planner Agent   │
                    │ Trip Intent     │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Attraction      │
                    │ Agent           │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Itinerary Agent │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Budget Agent    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Critic Agent    │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │ Final Itinerary │
                    └─────────────────┘
```

### Why an Agentic Workflow?

The main reason for separating the workflow was **responsibility and control**.

Each stage has a clear purpose, making it easier to:

* Understand what each part of the system is responsible for
* Modify one stage without rewriting the entire workflow
* Add additional validation or capabilities later
* Reason about where a problem occurred
* Keep deterministic calculations separate from probabilistic generation

---

## 🔄 End-to-End Flow

1. The user submits trip requirements through the application.
2. FastAPI converts the structured request into a natural-language planning query.
3. The Planner Agent extracts the main trip requirements.
4. The Attraction Agent generates attractions and activities.
5. The Itinerary Agent organizes them into a day-wise plan.
6. The Budget Agent evaluates the plan against a predefined expense model.
7. The Critic Agent combines the itinerary and budget information into the final output.
8. The final itinerary is returned to the user.
9. The generated plan can be exported as PDF or DOCX.

---

## 🧮 Deterministic Logic + LLM Reasoning

One of the design choices in this project was to avoid relying on the LLM for everything.

LLMs are useful for tasks such as:

* Understanding natural-language travel requests
* Generating attraction suggestions
* Organizing activities
* Reviewing plans
* Producing natural-language itineraries

Deterministic Python logic is used for tasks such as:

* Budget estimation
* Basic arithmetic
* Calculating total costs
* Generating downloadable files

This separation makes the system easier to reason about and reduces unnecessary reliance on probabilistic generation for calculations.

---

## 🌐 API

The application is exposed through a FastAPI backend.

### Generate a Trip

```http
POST /plan-trip
```

Example request:

```json
{
  "destination": "Goa",
  "days": 4,
  "people": 2,
  "budget": "mid",
  "travel_style": "solo"
}
```

The endpoint invokes the LangGraph workflow and returns the generated itinerary.

### Export PDF

```http
GET /export/pdf
```

Exports the latest generated itinerary as a PDF.

### Export DOCX

```http
GET /export/docx
```

Exports the latest generated itinerary as a Word document.

---

## 📄 Exporting Travel Plans

The generated itinerary can be exported into:

* PDF
* DOCX

This was added so that the output is not limited to the application's interface and can be saved or used outside the application.

---

## 🛠️ Tech Stack

| Layer               | Technology            |
| ------------------- | --------------------- |
| Language            | Python                |
| LLM                 | OpenAI GPT-4o-mini    |
| LLM Framework       | LangChain             |
| Agent Orchestration | LangGraph             |
| Backend             | FastAPI               |
| Data Validation     | Pydantic              |
| PDF Generation      | ReportLab             |
| DOCX Generation     | python-docx           |
| Frontend            | HTML, CSS, JavaScript |

---

## 📂 Project Structure

```text
agentic-travel-planner/
│
├── app/
│   │
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── attraction_agent.py
│   │   ├── itinerary_agent.py
│   │   ├── budget_agent.py
│   │   └── critic_agent.py
│   │
│   ├── utils/
│   │   ├── calculator.py
│   │   ├── expense_calculator.py
│   │   ├── export_pdf.py
│   │   └── export_docx.py
│   │
│   ├── static/
│   │   └── index.html
│   │
│   ├── api.py
│   └── graph.py
│
└── README.md
```

---

## 🔍 Key Product & Technical Decisions

### 1. Specialized agents instead of one large prompt

Breaking the workflow into multiple responsibilities makes the system easier to reason about and extend.

### 2. Deterministic budgeting

Budget estimates are generated using predefined expense categories rather than allowing the LLM to freely invent the baseline costs.

### 3. Shared state

LangGraph's state-based workflow allows information generated by one stage to become available to subsequent stages.

### 4. Simple user experience

The user only needs to provide basic trip requirements. The underlying agent workflow remains hidden from the user.

### 5. Exportable output

The itinerary can be converted into commonly used document formats so the generated plan can be taken outside the application.

---

## ⚠️ Limitations

This project is an exploration of agentic AI for travel planning and has several limitations.

### No live travel-data validation

The current version does not connect to live hotel, flight, attraction availability, or booking systems.

Therefore, generated recommendations and costs should not be treated as real-time booking information.

### Attraction recommendations

Attractions are generated by the LLM rather than being retrieved from a verified travel database.

### Budget estimates

The budget model uses predefined expense estimates for budget, mid-range, and luxury travel. Actual costs can vary significantly by destination, season, availability, and traveler preferences.

### In-memory storage

The latest itinerary is stored in memory for export. It is not designed as a multi-user persistent storage system.

---

## 🚀 What I Would Improve Next

If I continued developing the project, I would focus on making it more reliable and useful as a real travel product.

### 1. Add real travel data

Integrate external APIs for:

* Hotels
* Flights
* Attractions
* Maps and distances
* Real-time pricing

This would move the application from generated recommendations toward data-backed travel planning.

### 2. Add preference-based personalization

Allow users to specify preferences such as:

* Food preferences
* Activity interests
* Accessibility requirements
* Preferred pace
* Maximum daily travel time

The planner could then use these preferences when constructing the itinerary.

### 3. Add validation

Introduce validation between agent stages to check:

* Whether activities are geographically reasonable
* Whether the itinerary is overloaded
* Whether estimated costs are consistent
* Whether the plan fits the requested number of days

### 4. Improve evaluation

Create a structured evaluation framework to measure:

* Relevance of recommendations
* Itinerary quality
* Budget consistency
* User satisfaction
* Response reliability

### 5. Improve scalability

Replace in-memory itinerary storage with persistent storage and add proper user/session management for multiple users.

---

## 💭 What I Learned

The main learning from this project was that building an agentic application is less about simply adding multiple LLM calls and more about **deciding which parts of a problem should be handled by an LLM and which should remain deterministic.**

The project also helped me understand the importance of decomposing an ambiguous problem into smaller responsibilities.

For a production system, the next challenge would not simply be generating better itineraries. It would be making the recommendations **grounded in reliable data, geographically feasible, cost-aware, and measurable from a user-outcome perspective.**

---


## ⚠️ Disclaimer

This project is an experimental AI travel-planning application.

Recommendations, itineraries, and estimated costs are generated for planning purposes and should be independently verified before making travel or financial decisions.
