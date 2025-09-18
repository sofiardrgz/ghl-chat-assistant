import streamlit as st
from openai import OpenAI
import os


# Page config with custom title and icon
st.set_page_config(
    page_title="SmartSquatch", 
    page_icon="🦍",
    layout="wide"
)

# Custom header with logo and title
col1, col2 = st.columns([1, 4])
with col1:
    st.image("https://storage.googleapis.com/msgsndr/Wj3JvHTBsQKqvP85ShhE/media/68abc9cba7e59865de33aeaa.png", width=100)
with col2:
    st.title("SmartSquatch")
    st.caption("Your intelligent GHL assistant")

# Initialize OpenAI client
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception as e:
    st.error("Please set your OPENAI_API_KEY environment variable")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask me anything about your GHL data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Processing..."):
            try:
                response = client.responses.create(
                    model="gpt-5",
                    input=[{
                        "role": "developer",
                        "content": [{
                            "type": "input_text",
                            "text": f"The location id is {os.getenv('GHL_LOCATION_ID')}\n{prompt}"
                        }]
                    }],
                    text={"format": {"type": "text"}, "verbosity": "medium"},
                    reasoning={"effort": "medium"},
                    tools=[{
                        "type": "mcp",
                        "allowed_tools": [
                            "calendars_get-calendar-events", "calendars_get-appointment-notes",
                            "contacts_get-all-tasks", "contacts_add-tags", "contacts_remove-tags",
                            "contacts_get-contact", "contacts_update-contact", "contacts_upsert-contact",
                            "contacts_create-contact", "contacts_get-contacts", "conversations_search-conversation",
                            "conversations_get-messages", "conversations_send-a-new-message",
                            "locations_get-location", "locations_get-custom-fields",
                            "opportunities_search-opportunity", "opportunities_get-pipelines",
                            "opportunities_get-opportunity", "opportunities_update-opportunity",
                            "payments_get-order-by-id", "payments_list-transactions"
                        ],
                        "headers": {
                            "Authorization": os.getenv("GHL_AUTHORIZATION"),
                            "locationId": os.getenv("GHL_LOCATION_ID")
                        },
                        "require_approval": "always",
                        "server_label": "ghlmcp",
                        "server_url": os.getenv("GHL_SERVER_URL")
                    }]
                )
                
                st.markdown(response.text.content)
                st.session_state.messages.append({
                    "role": "assistant", 
                    "content": response.text.content
                })
                
            except Exception as e:
                st.error(f"Error: {str(e)}")
