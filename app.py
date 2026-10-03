import streamlit as st

# =========================================================
# CONVERSATION MEMORY
# =========================================================

if "conversation" not in st.session_state:
    st.session_state.conversation = []
if "email_status" not in st.session_state:
    st.session_state.email_status = ""
    
from agent import agent
from email_sender import send_email
from PIL import Image
import re
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# =========================================================
# PDF GENERATION
# =========================================================

def create_pdf(text):
    """Create a formatted PDF from the generated travel plan."""

    replacements = {
        "₹": "Rs.",
        "–": "-",
        "—": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
        "…": "...",
        "•": "-",
        "→": "->",
        "←": "<-",
        "✓": "[OK]",
        "✔": "[OK]",
        "\u00a0": " ",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.encode("latin-1", "replace").decode("latin-1")

    pdf_buffer = BytesIO()

    doc = SimpleDocTemplate(
        pdf_buffer,
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="AI Travel Planner",
        author="AI Travel Planner Agent",
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TravelTitle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        alignment=TA_CENTER,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "TravelSubtitle",
        parent=styles["Normal"],
        fontSize=10,
        leading=14,
        alignment=TA_CENTER,
        spaceAfter=15,
    )

    heading_style = ParagraphStyle(
        "TravelHeading",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True,
    )

    subheading_style = ParagraphStyle(
        "TravelSubHeading",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=15,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "TravelBody",
        parent=styles["BodyText"],
        fontSize=10,
        leading=15,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "TravelBullet",
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3,
    )

    table_header_style = ParagraphStyle(
        "TravelTableHeader",
        parent=body_style,
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
    )

    table_body_style = ParagraphStyle(
        "TravelTableBody",
        parent=body_style,
        fontSize=8,
        leading=10,
    )

    story = []

    def clean_markdown(line):
        line = line.replace("**", "")
        line = line.replace("__", "")
        line = line.replace("*", "")
        line = line.replace("_", "")
        return line.strip()

    def safe_text(line):
        return escape(clean_markdown(line))

    story.append(Paragraph("AI Travel Planner", title_style))
    story.append(Paragraph("Personalized Travel Plan", subtitle_style))

    lines = text.split("\n")
    i = 0

    while i < len(lines):

        line = lines[i].strip()

        if not line:
            story.append(Spacer(1, 4))
            i += 1
            continue

        # -------------------- Markdown tables --------------------

        if line.startswith("|") and "|" in line:

            table_rows = []

            while i < len(lines) and lines[i].strip().startswith("|"):

                row = lines[i].strip()

                if re.match(
                    r"^\|?\s*:?-+:?\s*(\|\s*:?-+:?\s*)+\|?$",
                    row,
                ):
                    i += 1
                    continue

                cells = [
                    clean_markdown(cell.strip())
                    for cell in row.strip("|").split("|")
                ]

                table_rows.append(cells)
                i += 1

            if table_rows:

                columns = max(len(row) for row in table_rows)

                for row in table_rows:
                    while len(row) < columns:
                        row.append("")

                available_width = A4[0] - 36 * mm
                col_width = available_width / columns

                formatted_rows = []

                for row_index, row in enumerate(table_rows):

                    formatted_row = []

                    for cell in row:

                        cell = escape(cell)

                        style = (
                            table_header_style
                            if row_index == 0
                            else table_body_style
                        )

                        formatted_row.append(
                            Paragraph(cell, style)
                        )

                    formatted_rows.append(formatted_row)

                table = Table(
                    formatted_rows,
                    repeatRows=1,
                    colWidths=[col_width] * columns,
                    hAlign="LEFT",
                )

                table.setStyle(
                    TableStyle(
                        [
                            (
                                "BACKGROUND",
                                (0, 0),
                                (-1, 0),
                                colors.lightgrey,
                            ),
                            (
                                "GRID",
                                (0, 0),
                                (-1, -1),
                                0.5,
                                colors.grey,
                            ),
                            (
                                "VALIGN",
                                (0, 0),
                                (-1, -1),
                                "TOP",
                            ),
                            (
                                "LEFTPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                            (
                                "RIGHTPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                            (
                                "TOPPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                            (
                                "BOTTOMPADDING",
                                (0, 0),
                                (-1, -1),
                                5,
                            ),
                        ]
                    )
                )

                story.append(Spacer(1, 6))
                story.append(table)
                story.append(Spacer(1, 8))

            continue

        # -------------------- Headings --------------------

        if line.startswith("### "):

            story.append(
                Paragraph(
                    safe_text(line[4:]),
                    heading_style,
                )
            )

            i += 1
            continue

        if line.startswith("#### "):

            story.append(
                Paragraph(
                    safe_text(line[5:]),
                    subheading_style,
                )
            )

            i += 1
            continue

        if re.match(r"^Day\s+\d+", line, re.IGNORECASE):

            story.append(
                Paragraph(
                    safe_text(line),
                    subheading_style,
                )
            )

            i += 1
            continue

        # -------------------- Bullets --------------------

        if line.startswith("- ") or line.startswith("* "):

            bullet = re.sub(r"^[-*]\s*", "", line)

            story.append(
                Paragraph(
                    "&#8226; " + safe_text(bullet),
                    bullet_style,
                )
            )

            i += 1
            continue

        # -------------------- Numbered sections --------------------

        if re.match(r"^\d+\.\s", line):

            story.append(
                Paragraph(
                    safe_text(line),
                    heading_style,
                )
            )

            i += 1
            continue

        # -------------------- Normal paragraph --------------------

        story.append(
            Paragraph(
                safe_text(line),
                body_style,
            )
        )

        i += 1

    def add_page_number(canvas, document):

        canvas.saveState()
        canvas.setFont("Helvetica", 8)

        canvas.drawCentredString(
            A4[0] / 2,
            10 * mm,
            f"AI Travel Planner  |  Page {document.page}",
        )

        canvas.restoreState()

    doc.build(
        story,
        onFirstPage=add_page_number,
        onLaterPages=add_page_number,
    )

    return pdf_buffer.getvalue()


# =========================================================
# STREAMLIT PAGE SETUP
# =========================================================

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
)


# =========================================================
# LOGO
# =========================================================

# logo = Image.open("assets/logo.png")
# st.image(logo, width=180)

# =========================================================
# PAGE HEADER
# =========================================================

# st.title("✈️ AI Travel Planner Agent")

# st.write(
#     "Plan smarter with AI-powered travel recommendations "
#     "using your travel guides."
# )

# =========================================================
# PAGE HEADER
# =========================================================

header_col1, header_col2 = st.columns([1, 5])

with header_col1:
    logo = Image.open("assets/logo.png")
    st.image(logo, width=110)
with header_col2:
    st.title("AI Travel Planner Agent") 
st.write(
    "Plan smarter with AI-powered travel recommendations "
    "using your travel guides."
)
# ✈️
# =========================================================
# TRIP DETAILS
# =========================================================

st.subheader("🧳 Your Trip Details")

destination = st.text_input(
    "📍 Destination",
    placeholder="e.g. Goa",
)

col1, col2 = st.columns(2)

with col1:
    days = st.number_input(
        "📅 Number of Days",
        min_value=1,
        max_value=30,
        value=4,
    )

with col2:
    budget = st.number_input(
        "💰 Budget (₹)",
        min_value=1000,
        value=25000,
        step=1000,
    )

email = st.text_input(
    "📧 Email",
    placeholder="example@gmail.com",
    key="email_input",
)
# st.write("EMAIL CHECK:", bool(email))
st.divider()


# =========================================================
# GENERATE AI TRAVEL PLAN
# =========================================================

if st.button(
    "✨ Generate Travel Plan",
    use_container_width=True,
):

    if not destination:
        st.warning("Please enter a destination.")

    else:

        user_query = f"""
        Plan a trip to {destination} for {days} days
        with a total budget of ₹{budget}.

        Use the travel guide knowledge base to provide:

        - Destination overview
        - Major tourist attractions
        - Best time to visit
        - Local food
        - Transportation
        - Accommodation areas
        - Approximate budget guidance
        - Safety and travel tips
        - Local culture
        - Suggested activities
        - Important practical information
        - A day-by-day itinerary

        Keep the plan practical and within the given budget.
        """

        with st.spinner("✈️ Creating your travel plan..."):

            try:

                # response = agent.invoke(
                #     {
                #         "messages": [
                #             {
                #                 "role": "user",
                #                 "content": user_query,
                #             }
                #         ]
                #     }
                # )
                # Save the user's original travel request
                st.session_state.conversation.append(
                    {
                        "role": "user",
                        "content": user_query,
                    }
                )   

                # Send the conversation to the agent
                response = agent.invoke(
                    {
                        "messages": st.session_state.conversation
                    }
                )


            except Exception as e:

                error_message = str(e)

                if (
                    "RESOURCE_EXHAUSTED" in error_message
                    or "429" in error_message
                ):

                    st.error(
                        "⚠️ Gemini API quota reached. "
                        "Please try again later."
                    )

                else:

                    st.error(
                        f"⚠️ Error: {e}"
                    )

                st.stop()

        # -----------------------------------------------------
        # Extract final answer
        # -----------------------------------------------------

        final_answer = response["messages"][-1].content

        if isinstance(final_answer, list):

            text_parts = []

            for block in final_answer:

                if (
                    isinstance(block, dict)
                    and block.get("type") == "text"
                ):
                    text_parts.append(
                        block.get("text", "")
                    )

                elif isinstance(block, str):
                    text_parts.append(block)

            final_answer = "\n".join(text_parts)
        # Save the AI response to conversation memory
        st.session_state.conversation.append(
            {
                "role": "assistant",
                "content": final_answer,
            }
        )

        # -----------------------------------------------------
        # Display result
        # -----------------------------------------------------

        st.success(
            "🎉 Your travel plan is ready!"
        )

        st.divider()

        st.subheader(
            "🗺️ Your Travel Plan"
        )

        st.markdown(final_answer)

        # -----------------------------------------------------
        # Generate PDF
        # -----------------------------------------------------

        pdf_data = create_pdf(final_answer)

        # Send Email
        if email:
            st.info("📧 Trying to send email...")

            try:
                send_email(
                    email.strip(),
                    f"Your {destination} Travel Plan",
                    final_answer
                )

                # st.success("📧 Travel plan sent to your email!")
                st.session_state.email_status = "📧 Travel plan sent to your email!"
                # st.success(st.session_state.email_status)

            except Exception as e:
                st.session_state.email_status = ""
                st.error(f"⚠️ Email error: {e}")
            
        st.download_button(
            label="⬇️ Download Travel Plan as PDF",
            data=pdf_data,
            file_name=f"{destination}_Travel_Plan.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

# =========================================================
# PERSIST EMAIL STATUS
# =========================================================

if st.session_state.email_status:
    st.success(st.session_state.email_status)
            
# =========================================================
# FOLLOW-UP QUESTIONS
# =========================================================

st.divider()

st.subheader("💬 Ask a Follow-up")

follow_up = st.text_input(
    "Ask something about your travel plan",
    placeholder="e.g. Make Day 2 cheaper"
)
if st.button("💬 Ask", use_container_width=True):

    if not follow_up.strip():

        st.warning("Please enter a follow-up question.")

    else:

        # Add follow-up question to conversation
        st.session_state.conversation.append(
            {
                "role": "user",
                "content": follow_up,
            }
        )

        with st.spinner("🤔 Thinking..."):

            try:
                response = agent.invoke(
                    {
                        "messages": st.session_state.conversation
                    }
                )

            except Exception as e:

                error_message = str(e)

                if (
                    "RESOURCE_EXHAUSTED" in error_message
                    or "429" in error_message
                ):
                    st.error(
                        "⚠️ Gemini API quota reached. "
                        "Please try again later."
                    )
                else:
                    st.error(f"⚠️ Error: {e}")

                st.stop()

        follow_up_answer = response["messages"][-1].content

        if isinstance(follow_up_answer, list):

            text_parts = []

            for block in follow_up_answer:

                if (
                    isinstance(block, dict)
                    and block.get("type") == "text"
                ):
                    text_parts.append(
                        block.get("text", "")
                    )

                elif isinstance(block, str):
                    text_parts.append(block)

            follow_up_answer = "\n".join(text_parts)

        # Save AI follow-up response
        st.session_state.conversation.append(
            {
                "role": "assistant",
                "content": follow_up_answer,
            }
        )
        st.subheader("💬 Follow-up Answer")
        st.markdown(follow_up_answer)

