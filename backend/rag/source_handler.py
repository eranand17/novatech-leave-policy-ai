import re


SECTIONS = [
    "Purpose",
    "Scope",
    "Leave Year",
    "Types of Leave",
    "Earned Leave (EL)",
    "Casual Leave (CL)",
    "Sick Leave (SL)",
    "Optional Holiday (OH)",
    "Bereavement Leave (BL)",
    "Paternity Leave (PL)",
    "Maternity Leave (ML)",
    "Compensatory Off (CO)",
    "Leave Without Pay (LWP)",
    "Leave During Probation",
    "Leave Application Process",
    "Emergency Leave",
    "Leave Approval",
    "Unauthorized Absence",
    "Leave Cancellation",
    "Public Holidays",
    "Leave Balance Example",
    "Frequently Asked Questions",
]


KEYWORDS = {
    "Earned Leave (EL)": ["earned leave", "45 days"],
    "Casual Leave (CL)": ["casual leave", "3 consecutive"],
    "Sick Leave (SL)": ["sick leave", "medical documentation"],
    "Optional Holiday (OH)": ["optional holiday"],
    "Bereavement Leave (BL)": ["bereavement leave"],
    "Paternity Leave (PL)": ["paternity leave"],
    "Maternity Leave (ML)": ["maternity leave"],
    "Compensatory Off (CO)": ["compensatory off", "comp-off", "compensatory leave"],
    "Leave Without Pay (LWP)": ["leave without pay", "lwp"],
    "Leave During Probation": ["leave during probation", "probation period"],
    "Leave Application Process": ["leave application process", "leave balance update"],
    "Emergency Leave": ["emergency leave", "same-day"],
    "Leave Approval": ["leave approval", "reporting manager"],
    "Unauthorized Absence": ["unauthorized absence", "discipline"],
    "Leave Cancellation": ["leave cancellation", "cancel leave"],
    "Public Holidays": ["public holidays", "holiday calendar"],
    "Leave Balance Example": ["leave balance example", "rahul"],
    "Frequently Asked Questions": ["frequently asked questions", "faq"],
}


def clean(text):
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip().lower()


def find_section(text):
    text = clean(text)
    if "reporting manager" in text and "approved" in text:
        return "Leave Approval"

    # Exact numbered heading
    for section in SECTIONS:
        name = re.sub(r"\s*\([^)]*\)", "", section).lower()
        if re.search(rf"\b\d{{1,2}}\.\s*{re.escape(name)}\b", text):
            return section

    # Heading without number
    for section in SECTIONS:
        name = re.sub(r"\s*\([^)]*\)", "", section).lower()

        if section in ["Purpose", "Scope", "Leave Year"]:
            continue

        if re.search(rf"\b{re.escape(name)}\b", text):
            return section

    # Keyword fallback
    best = None
    score = 0

    for section, words in KEYWORDS.items():
        current = sum(word.lower() in text for word in words)

        if current > score:
            score = current
            best = section

    return best or "Policy Document"


def create_source_info(documents):
    sources = []
    seen = set()

    for doc in documents:
        page = doc.metadata.get("page")

        if page is not None:
            page += 1

        section = find_section(doc.page_content)
        key = (page, section)

        if key not in seen:
            sources.append({
                "page": page,
                "section": section
            })
            seen.add(key)

    return sources


def format_sources(sources):
    if not sources:
        return "No source reference available."

    return "\n".join(
        f"{i}. {s['section']} — Page {s['page']}"
        for i, s in enumerate(sources, 1)
    )


if __name__ == "__main__":
    print("SOURCE HANDLER TEST\n")

    tests = [
        ("12. Compensatory Off (CO)\nComp-Off should normally be used within 60 days.",
         6),
        ("7. Sick Leave (SL)\nEmployees receive 10 days of Sick Leave.",
         4),
        ("4. Types of Leave\nEarned Leave, Casual Leave, Sick Leave.",
         2),
    ]

    for text, page in tests:
        doc = type(
            "Document",
            (),
            {
                "page_content": text,
                "metadata": {"page": page - 1}
            }
        )()

        print(format_sources(create_source_info([doc])))

    print("\nTEST COMPLETED")