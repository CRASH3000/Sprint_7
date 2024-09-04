expected_responses = {
    "courier": {
        "create_success": {"ok": True},
        "duplicate_error": {"code": 409, "message": "Этот логин уже используется"},
        "missing_field_error": {"code": 400, "message": "Недостаточно данных для создания учетной записи"},
    },

    "courier_login": {
        "missing_error": {"code": 400, "message": "Недостаточно данных для входа"},
        "login_error": {"code": 404, "message": "Учетная запись не найдена"},
    },

     "delete_courier": {
        "without_id_error": {"code": 400, "message": "Недостаточно данных для удаления курьера"},
        "nonexistent_id_error": {"code": 404, "message": "Курьера с таким id нет"},
    }
}