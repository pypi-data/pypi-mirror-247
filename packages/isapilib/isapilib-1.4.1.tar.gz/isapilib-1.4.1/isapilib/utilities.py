from django.db import connections


def execute_query(query, sp_params=None, using='default'):
    cursor = connections[using].cursor()

    try:
        cursor.execute(query, sp_params or [])
        results = cursor.fetchall()
    finally:
        cursor.close()

    return results


def execute_sp(sp_name, sp_params=None, using='default'):
    if sp_params:
        sp_call = f"EXEC {sp_name} {', '.join('%s' for _ in sp_params)}"
    else:
        sp_call = f"EXEC {sp_name}"

    return execute_query(sp_call, sp_params, using)
