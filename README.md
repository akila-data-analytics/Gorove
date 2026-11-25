# 🌍 GoRove – AI-Powered Intelligent Travel Planner

GoRove is an AI-powered travel planning application built using Python, Streamlit, Google Gemini AI, and SQLite. It helps users explore destinations, plan trips, estimate travel expenses, generate day-wise itineraries, and search flight and hotel information through a conversational travel assistant.

The application follows a **Multi-Agent Architecture**, where five specialized agents handle different travel-related tasks.

---

## 🎯 Project Objective

The objective of GoRove is to simplify travel planning by bringing multiple travel assistance features into a single application.

Instead of manually searching for destinations, hotels, activities, and travel costs, users can interact with an intelligent travel assistant to receive organized travel information and planning support.

---

## ✨ Key Features

### 1. AI Travel Assistant
- Conversational travel assistance using Google Gemini AI.
- Understands general travel-related queries.
- Provides destination guidance.
- Uses local Python-based fallback responses when Gemini is unavailable.

### 2. Destination Research
- Explore available travel destinations.
- View destination descriptions and categories.
- Get recommended hotels and activities.
- View estimated destination costs and recommended visiting seasons.

### 3. Trip Planner
- Enter trip details and travel preferences.
- Explore destination recommendations.
- Plan trips based on travel requirements.

### 4. Flight Search
- Search flight information using origin and destination.
- View airline, flight number, departure time, arrival time, travel date, and price.
- Compare available flight prices from the local database.

### 5. Hotel Search
- Explore hotels based on destination.
- View hotel location, price per night, and rating.
- Compare available hotel options.

### 6. Travel Budget Planner
- Estimate accommodation expenses.
- Calculate food and transportation costs.
- Include activity and other expenses.
- Compare estimated expenses with the user's budget.
- Calculate per-person travel costs.

### 7. Itinerary Generator
- Generate day-wise travel itineraries.
- Organize activities into morning, afternoon, and evening.
- Include leisure time, food recommendations, and travel tips.

### 8. User Management
- User registration and login.
- Password hashing using bcrypt.
- Customer account management.
- Saved trip management.

### 9. Admin Dashboard
- View user and trip summaries.
- Manage customer accounts.
- Update customer account status.
- Manage trip status.

### 10. Additional Features
- My Trips
- My Profile
- Cancellation & Refund Policy
- Privacy Policy
- Terms & Conditions
- Frequently Asked Questions

---

## 🤖 Multi-Agent Architecture

GoRove uses five specialized agents coordinated through a central `TravelAgentManager`.

| Agent | Responsibility |
|---|---|
| Travel Assistant Agent | Main conversational assistant using Gemini AI |
| Destination Research Agent | Retrieves destination, hotel, and activity information |
| Budget Analyst Agent | Calculates estimated travel expenses |
| Itinerary Planner Agent | Creates day-wise travel itineraries |
| Booking Assistant Agent | Searches and compares flight and hotel records |

### Agent Workflow

```text
                 User
                   |
                   v
           Streamlit Frontend
                   |
                   v
           TravelAgentManager
                   |
          Request Classification
                   |
          +--------+--------+
          |        |        |
          v        v        v
       Travel  Destination  Budget
      Assistant Research   Analyst
          |        |        |
          +--------+--------+
                   |
          +--------+--------+
          |                 |
          v                 v
      Itinerary           Booking
       Planner           Assistant
          |                 |
          +--------+--------+
                   |
          Gemini AI / SQLite
                   |
                   v
             User Response
```

---

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| Streamlit | Frontend and user interface |
| Google Gemini AI | AI-powered conversational responses |
| Google Gen AI SDK | Gemini API integration |
| SQLite | Database management |
| SQL | Database queries and operations |
| bcrypt | Password hashing |
| python-dotenv | Environment variable management |
| Regular Expressions | Extract travel details from user requests |

---

## 🗄️ Database Design

GoRove uses SQLite for storing application and travel-related information.

The database contains seven tables:

| Table | Description |
|---|---|
| users | Customer and admin account information |
| destinations | Destination details |
| hotels | Hotel information and pricing |
| activities | Destination activities and estimated costs |
| flights | Flight information and pricing |
| trips | User trip records |
| itineraries | Saved day-wise itinerary information |

### Sample Travel Dataset

The project includes sample travel information for:

- 10 Destinations
- 15 Hotels
- 20 Activities
- 15 Flight Records

**Total: 60 sample travel records.**

Sample destinations include Ooty, Kodaikanal, Munnar, Coorg, Goa, Jaipur, Manali, Pondicherry, Wayanad, and Alleppey.

*Note: Flight and hotel information is retrieved from the application's local database. The application does not perform live airline or hotel bookings.*

---

## 📁 Project Structure

```text
AI_Travel_Planner_Agent/
│
├── agents/
│   ├── __init__.py
│   ├── agent_manager.py
│   ├── travel_assistant_agent.py
│   ├── destination_research_agent.py
│   ├── budget_analyst_agent.py
│   ├── itinerary_planner_agent.py
│   └── booking_assistant_agent.py
│
├── database/
│   ├── db_connection.py
│   ├── db_setup.py
│   └── sample_data.py
│
├── services/
│   ├── __init__.py
│   ├── admin_setup.py
│   ├── auth_service.py
│   ├── database_service.py
│   └── gemini_service.py
│
├── app.py
├── requirements.txt
├── README.md
│
├── test_agent_manager.py
├── test_auth.py
└── test_gemini.py
```

---

## ⚙️ Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <your-github-repository-url>
```

### Step 2: Navigate to the Project Folder

```bash
cd AI_Travel_Planner_Agent
```

### Step 3: Create a Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate the Virtual Environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 6: Configure Gemini API

Create a `.env` file in the project root directory.

Add the following configuration:

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

Replace `your_gemini_api_key` with your actual Gemini API key.

**Important:** Never upload your `.env` file or API key to GitHub.

### Step 7: Initialize the Database

Run the following commands from the project root:

```bash
python -c "from database.db_setup import create_tables; create_tables()"
```

```bash
python database/sample_data.py
```

The first command creates the database tables. The second inserts sample destination, hotel, activity, and flight records.

### Step 8: Create an Admin Account

```bash
python -m services.admin_setup
```

Follow the terminal instructions to create your admin account.

### Step 9: Run the Application

```bash
streamlit run app.py
```

The GoRove application will open in your browser.

---

## 🧪 Testing

The project includes separate test files for important application components.

Run the tests using:

```bash
python test_agent_manager.py
```

```bash
python test_auth.py
```

```bash
python test_gemini.py
```

---

## 🔐 Security

- Passwords are hashed using bcrypt.
- Authentication is handled through a dedicated authentication service.
- Environment variables are used to store the Gemini API key.
- Database operations use parameterized SQL queries.
- Customer and admin roles are maintained in the database.

---

## 🚀 Future Enhancements

- Live flight and hotel booking integrations.
- Real-time travel price information.
- Interactive maps and route planning.
- Weather-based destination recommendations.
- Advanced personalized travel recommendations.

---

## 👩‍💻 Project Information

**Project Name:** GoRove – AI-Powered Intelligent Travel Planner

**Domain:** Artificial Intelligence / Travel Technology

**Architecture:** Multi-Agent Architecture

**Frontend:** Streamlit

**Backend:** Python

**AI Integration:** Google Gemini AI

**Database:** SQLite

---

## 📌 Disclaimer

GoRove is an educational and portfolio project. Travel prices, hotel details, activities, and flight information are based on the application's sample SQLite database and should not be considered live booking or availability information.

---

**GoRove – Plan Smarter. Explore Better. Travel Happier! 🌍**
