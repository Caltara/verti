import streamlit as st
import openai
from datetime import datetime, date, time

# Set your OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title="Verti - Your Personal AI Assistant", layout="wide")
st.title("Verti - Your Personal AI Assistant 🤖")

# Initialize session state for storing data temporarily
if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "reminders" not in st.session_state:
    st.session_state.reminders = []

if "meetings" not in st.session_state:
    st.session_state.meetings = []

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "trips" not in st.session_state:
    st.session_state.trips = []

def ask_gpt(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content.strip()

feature = st.sidebar.selectbox("Choose a feature", [
    "Plan Business Trip",
    "Draft Correspondence",
    "Coordinate Meetings",
    "Meeting Follow-ups",
    "Project Management",
    "Offload Routine Tasks",
    "Expense Tracking & Reporting",
    "Reminders & Alerts",
    "Document Summarization",
    "Task Prioritization Assistant",
    "Data Dashboard"
])

if feature == "Plan Business Trip":
    st.header("Plan Your Business Trip")
    destination = st.text_input("Destination city/country")
    start_date = st.date_input("Start date")
    end_date = st.date_input("End date")
    preferences = st.text_area("Preferences (e.g. preferred airlines, hotel types, budget)")

    if st.button("Create Trip Plan"):
        prompt = f"""
        You are an AI assistant named Verti. Plan a detailed business trip to {destination} from {start_date} to {end_date}.
        Consider flights, accommodations, transport, and daily itinerary.
        Preferences: {preferences}.
        """
        result = ask_gpt(prompt)
        st.success("Here is your business trip plan:")
        st.write(result)
        st.session_state.trips.append({
            "destination": destination,
            "start_date": str(start_date),
            "end_date": str(end_date),
            "summary": result,
        })

elif feature == "Draft Correspondence":
    st.header("Draft Your Correspondence")
    email_type = st.selectbox("Type of correspondence", ["Business Email", "Thank You Note", "Follow-up Email", "Meeting Request"])
    context = st.text_area("Context or details for the email")

    if st.button("Draft Email"):
        prompt = f"Verti, draft a professional {email_type.lower()} with the following details:\n{context}"
        draft = ask_gpt(prompt)
        st.success("Drafted Email:")
        st.text_area("Your Draft", draft, height=200)

elif feature == "Coordinate Meetings":
    st.header("Coordinate Your Meetings")
    meeting_date = st.date_input("Meeting Date")
    meeting_time = st.time_input("Meeting Time")
    participants = st.text_area("List of participants (names, roles, emails)")
    agenda_points = st.text_area("Proposed agenda points")

    if st.button("Generate Meeting Plan"):
        prompt = f"""
        Verti, create a meeting plan for a meeting on {meeting_date} at {meeting_time}.
        Participants: {participants}.
        Agenda: {agenda_points}.
        Include agenda, roles, and minutes template.
        """
        meeting_plan = ask_gpt(prompt)
        st.success("Meeting Plan:")
        st.write(meeting_plan)
        st.session_state.meetings.append({
            "date": str(meeting_date),
            "time": str(meeting_time),
            "participants": participants,
            "agenda": agenda_points,
            "plan": meeting_plan,
        })

elif feature == "Meeting Follow-ups":
    st.header("Draft Meeting Follow-Up Email")
    if not st.session_state.meetings:
        st.info("No meetings found yet. Please schedule meetings under 'Coordinate Meetings' first.")
    else:
        selected_meeting = st.selectbox("Select Meeting to Follow Up", options=[f"{m['date']} - {m['agenda'][:30]}..." for m in st.session_state.meetings])
        index = [f"{m['date']} - {m['agenda'][:30]}..." for m in st.session_state.meetings].index(selected_meeting)
        meeting = st.session_state.meetings[index]

        additional_notes = st.text_area("Additional notes or points to include in follow-up")

        if st.button("Draft Follow-Up Email"):
            prompt = f"""
            Verti, draft a professional follow-up email for the meeting held on {meeting['date']} at {meeting['time']}.
            Participants: {meeting['participants']}.
            Agenda: {meeting['agenda']}.
            Meeting summary or plan: {meeting['plan']}.
            Additional notes: {additional_notes}.
            """
            follow_up_email = ask_gpt(prompt)
            st.success("Follow-Up Email Draft:")
            st.text_area("Your Draft", follow_up_email, height=200)

elif feature == "Project Management":
    st.header("Project Management Support")
    project_name = st.text_input("Project Name")
    project_goals = st.text_area("Project goals and objectives")
    current_status = st.text_area("Current project status")
    challenges = st.text_area("Challenges or blockers")

    if st.button("Get Project Advice"):
        prompt = f"""
        Verti is a project manager assistant. The project is named '{project_name}'.
        Goals: {project_goals}.
        Current status: {current_status}.
        Challenges: {challenges}.
        Provide advice on how to proceed, prioritize tasks, and manage resources effectively.
        """
        advice = ask_gpt(prompt)
        st.success("Project Advice:")
        st.write(advice)
        st.session_state.tasks.append({
            "project": project_name,
            "goals": project_goals,
            "status": current_status,
            "advice": advice
        })

elif feature == "Offload Routine Tasks":
    st.header("Automate Routine Tasks")
    task_description = st.text_area("Describe the repetitive task you want to automate")

    if st.button("Get Automation Suggestions"):
        prompt = f"""
        Verti, suggest ways to automate the following repetitive administrative task:
        {task_description}
        Provide step-by-step guidance or tools to use.
        """
        automation_plan = ask_gpt(prompt)
        st.success("Automation Plan:")
        st.write(automation_plan)

elif feature == "Expense Tracking & Reporting":
    st.header("Track Business Trip Expenses")
    with st.form("expense_form"):
        date_expense = st.date_input("Date")
        item = st.text_input("Expense Item")
        amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
        category = st.selectbox("Category", ["Flight", "Hotel", "Meals", "Transport", "Misc"])
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            st.session_state.expenses.append({
                "date": str(date_expense),
                "item": item,
                "amount": amount,
                "category": category,
            })
            st.success(f"Added expense: {item} - ${amount:.2f}")

    if st.session_state.expenses:
        if st.button("Summarize Expenses"):
            expenses_text = "\n".join([f"{e['date']}, {e['item']}, {e['amount']}, {e['category']}" for e in st.session_state.expenses])
            prompt = f"""
            Verti, summarize these business trip expenses and categorize totals by category:
            {expenses_text}
            """
            summary = ask_gpt(prompt)
            st.success("Expense Summary:")
            st.write(summary)

elif feature == "Reminders & Alerts":
    st.header("Manage Reminders & Alerts")
    with st.form("reminder_form"):
        reminder_text = st.text_input("Reminder Description")
        reminder_date = st.date_input("Reminder Date", min_value=date.today())
        reminder_time = st.time_input("Reminder Time")
        submitted = st.form_submit_button("Add Reminder")
        if submitted:
            reminder_datetime = datetime.combine(reminder_date, reminder_time)
            st.session_state.reminders.append({
                "text": reminder_text,
                "datetime": reminder_datetime
            })
            st.success(f"Added reminder for {reminder_datetime.strftime('%Y-%m-%d %H:%M')}")

    if st.session_state.reminders:
        st.subheader("Upcoming Reminders")
        for r in sorted(st.session_state.reminders, key=lambda x: x["datetime"]):
            dt_str = r["datetime"].strftime('%Y-%m-%d %H:%M')
            st.write(f"- {dt_str}: {r['text']}")

elif feature == "Document Summarization":
    st.header("Summarize Documents or Emails")
    document_text = st.text_area("Paste document or email content")

    if st.button("Summarize"):
        prompt = f"Verti, summarize the following text professionally and concisely:\n{document_text}"
        summary = ask_gpt(prompt)
        st.success("Summary:")
        st.write(summary)

elif feature == "Task Prioritization Assistant":
    st.header("Task Prioritization Assistant")
    tasks_text = st.text_area("Enter your tasks, one per line")

    if st.button("Prioritize Tasks"):
        prompt = f"""
        Verti, here is a list of tasks:\n{tasks_text}\n
        Please prioritize them based on urgency and impact and provide a ranked list with brief reasoning.
        """
        prioritized_tasks = ask_gpt(prompt)
        st.success("Prioritized Tasks:")
        st.write(prioritized_tasks)
        st.session_state.tasks.append({
            "tasks": tasks_text,
            "prioritization": prioritized_tasks
        })

elif feature == "Data Dashboard":
    st.header("Verti Data Dashboard")
    st.subheader("Trips")
    if st.session_state.trips:
        for i, trip in enumerate(st.session_state.trips, 1):
            st.markdown(f"**Trip {i}:** {trip['destination']} ({trip['start_date']} to {trip['end_date']})")
            with st.expander("View Trip Summary"):
                st.write(trip['summary'])
    else:
        st.write("No trips logged yet.")

    st.subheader("Meetings")
    if st.session_state.meetings:
        for i, m in enumerate(st.session_state.meetings, 1):
            st.markdown(f"**Meeting {i}:** {m['date']} at {m['time']}")
            st.write(f"Participants: {m['participants']}")
            with st.expander("View Agenda / Plan"):
                st.write(m['agenda'])
                st.write(m['plan'])
    else:
        st.write("No meetings logged yet.")

    st.subheader("Expenses")
    if st.session_state.expenses:
        total = sum(e["amount"] for e in st.session_state.expenses)
        st.write(f"Total expenses logged: ${total:.2f}")
        if st.button("Show all expenses"):
            for e in st.session_state.expenses:
                st.write(f"{e['date']}: {e['item']} - ${e['amount']:.2f} ({e['category']})")
    else:
        st.write("No expenses logged yet.")

    st.subheader("Tasks & Projects")
    if st.session_state.tasks:
        for i, t in enumerate(st.session_state.tasks, 1):
            if "project" in t:
                st.markdown(f"**Project {i}:** {t['project']}")
                st.write(f"Goals: {t['goals']}")
                st.write(f"Status: {t['status']}")
                with st.expander("Advice"):
                    st.write(t['advice'])
            else:
                st.markdown(f"**Task Batch {i}:**")
                st.write("Tasks:")
                st.write(t.get("tasks", ""))
                with st.expander("Prioritization"):
                    st.write(t.get("prioritization", ""))
    else:
        st.write("No tasks or projects logged yet.")

    st.subheader("Reminders")
    if st.session_state.reminders:
        for r in sorted(st.session_state.reminders, key=lambda x: x["datetime"]):
            dt_str = r["datetime"].strftime('%Y-%m-%d %H:%M')
            st.write(f"- {dt_str}: {r['text']}")
    else:
        st.write("No reminders set.")

st.sidebar.markdown("---")
st.sidebar.write("Made with ❤️ by Verti AI Assistant")
