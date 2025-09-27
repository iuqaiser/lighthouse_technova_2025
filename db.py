from backend import conn

def search_therapists(
    gender=None, therapy_type=None, trauma_focus=None, insurance=None, max_cost=None
):
    cur = conn.cursor()
    query = "SELECT * FROM therapists WHERE 1=1"
    params = []

    if gender:
        query += " AND gender = %s"
        params.append(gender)
    if therapy_type:
        query += " AND ARRAY_CONTAINS(%s, therapy_types)"
        params.append(therapy_type)
    if trauma_focus:
        query += " AND ARRAY_CONTAINS(%s, trauma_focus)"
        params.append(trauma_focus)
    if insurance:
        query += " AND ARRAY_CONTAINS(%s, insurance_accepted)"
        params.append(insurance)
    if max_cost:
        query += " AND session_cost <= %s"
        params.append(max_cost)

    cur.execute(query, params)
    results = cur.fetchall()
    cur.close()
    return results
