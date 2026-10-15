import json

from retrieval.retrieval_engine import RetrievalEngine
from rag.llm_engine import generate_answer
from rag.verification import VerificationEngine

from database.postgres_db import (
    connect_db,
    get_all_employees,
    get_employee_by_name
)


def load_documents():

    with open("embeddings/embeddings.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    docs = []
    metadata = []

    for item in data:
        docs.append(item["text"])
        metadata.append(item["pdf_name"])

    return docs, metadata


# ----------------------------
# SQL QUERY DETECTOR
# ----------------------------

def is_employee_query(query):

    keywords = [
        "employee",
        "salary",
        "department",
        "join year",
        "joined",
        "staff"
    ]

    q = query.lower()

    return any(word in q for word in keywords)


# ----------------------------
# HANDLE SQL QUESTIONS
# ----------------------------

def handle_employee_query(query):

    from database.postgres_db import (
        connect_db,
        initialize_database,
        get_all_employees,
        get_employee_by_name,
        get_department_employees,
        get_highest_salary_employee
    )

    initialize_database()
    conn = connect_db()

    q = query.lower()

    try:
        if "all employees" in q:
            rows = get_all_employees(conn)
            return "\n".join([f"{r.name} - {r.department}" for r in rows[:20]])

        elif "highest salary" in q:
            emp = get_highest_salary_employee(conn)
            return f"{emp.name} has highest salary: {emp.salary}"

        elif "engineering" in q:
            rows = get_department_employees(conn, "Engineering")
            return "\n".join([r.name for r in rows[:10]])

        else:
            rows = get_all_employees(conn)

            for emp in rows:
                if emp.name.lower() in q:

                    sql_context = f"""
                    Employee Name: {emp.name}
                    Department: {emp.department}
                    Join Year: {emp.join_year}
                    Salary: ₹{emp.salary:,.2f}
                    """

                    return generate_answer(query, sql_context)

        return "Employee found but query not matched."

    finally:
        conn.close()


# ----------------------------
# MAIN PIPELINE
# ----------------------------

def ask_question(query, method="hybrid"):

    # Route to SQL
    if is_employee_query(query):

        answer = handle_employee_query(query)

        return {
            "answer": answer,
            "chunks": [],
            "pdf": ["PostgreSQL Database"],
            "verification": {
                "status": "Verified",
                "confidence": 1.0
            }
        }

    # RAG route
    docs, meta = load_documents()

    retriever = RetrievalEngine(docs)

    indices = retriever.search(query, method=method, top_k=3)

    chunks = []
    pdf_sources = []

    for i in indices:
        chunks.append(docs[i])
        pdf_sources.append(meta[i])

    context = "\n".join(chunks)

    answer = generate_answer(query, context)

    verifier = VerificationEngine(retriever)

    verification = verifier.verify_answer(answer)

    return {
        "answer": answer,
        "chunks": chunks,
        "pdf": list(set(pdf_sources)),
        "verification": verification
    }