import streamlit as st
from google import genai

# Page Config
st.set_page_config(
    page_title="Byway Partner Generator",
    page_icon="🚆",
    layout="wide"
)

# Title & Header
st.title("🚆 Byway Partner Outreach & Pitch Generator")
st.caption("Generate tailored pitch emails, co-marketing ideas, and executive one-pagers powered by Byway context.")

# Sidebar for API Key
with st.sidebar:
    st.header("⚙️ Configuration")
    if "GEMINI_API_KEY" in st.secrets:
        api_key = st.secrets["GEMINI_API_KEY"]
        st.success("✅ Gemini API Key loaded!")
    else:
        api_key = st.text_input("Enter Gemini API Key", type="password")

# Form Inputs based on JSON Schema
with st.form("partner_form"):
    
    st.subheader("1. Task Selection")
    output_type = st.selectbox(
        "Select output type*",
        ["Tailored pitch email", "Co-marketing campaign ideas", "Internal executive one-pager"]
    )
    
    st.markdown("---")
    
    st.subheader("2. Partner Details")
    col1, col2 = st.columns(2)
    with col1:
        partner_name = st.text_input(
            "Partner organization name*",
            placeholder="e.g. National Geographic Traveller, Trailfinders"
        )
    with col2:
        partner_category = st.selectbox(
            "Partner category*",
            [
                "Travel agent / Retail network",
                "Affiliate / Media publisher",
                "Tour operator / Referral partner",
                "Accommodation supplier",
                "Rail / Transport provider"
            ]
        )
    target_audience = st.text_input(
        "Partner target audience / Customer profile",
        placeholder="e.g. Eco-conscious professionals, UK retirees, luxury travellers"
    )
    
    st.markdown("---")
    
    st.subheader("3. Commercial & Proposal Context")
    proposed_structure = st.text_input(
        "Proposed commercial structure",
        placeholder="e.g. 10% base commission, 3% referral fee, API integration"
    )
    key_value_driver = st.text_area(
        "Primary hook or strategic objective*",
        placeholder="e.g. Expand non-flight European packages, launch joint summer campaign, diversify accommodation supply away from single-supplier dependence"
    )
    additional_notes = st.text_area(
        "Known risks, operational considerations, or sensitivities",
        placeholder="e.g. Requires custom API dev, client accepting liability, strict booking flow demands"
    )

    submit = st.form_submit_button("🚀 Generate Partner Asset", use_container_width=True)

# Processing Output
if submit:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar or save it in Streamlit secrets.")
    elif not partner_name or not key_value_driver:
        st.warning("Please fill in all required fields (Partner Name & Primary Hook).")
    else:
        system_instruction = """
        You are an expert Strategic Partnerships Lead at Byway, the flight-free travel platform. 
        Your tone is warm, professional, mission-driven (sustainable travel made simple), and commercially sharp.
        
        Always frame Byway's key strengths: 100% flight-free multi-modal trips (train/ferry), seamless journey planning, 
        ABTA protection, and exceptional customer experience.
        """
        
        user_prompt = f"""
        Task: Create a **{output_type}** for a prospective partnership.
        
        Context Details:
        - Partner Name: {partner_name}
        - Category: {partner_category}
        - Partner Audience: {target_audience if target_audience else 'Not specified'}
        - Proposed Commercial Structure: {proposed_structure if proposed_structure else 'Standard terms'}
        - Primary Strategic Hook: {key_value_driver}
        - Considerations/Sensitivities: {additional_notes if additional_notes else 'None'}
        
        Provide a polished, complete output ready to be shared or sent.
        """

        with st.spinner("Crafting your partnership asset with Gemini..."):
            try:
                # Initialize Gemini client
                client = genai.Client(api_key=api_key)
                
                # Generate content using Gemini 3 Flash
                response = client.models.generate_content(
                    model='gemini-2.0-flash',
                    contents=user_prompt,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7
                    )
                )
                
                st.markdown("---")
                st.subheader(f"📄 Result: {output_type}")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
