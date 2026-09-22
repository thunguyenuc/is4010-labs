def calculate_average_age(users):
    """Return the average numeric age, or 0.0 when none are valid."""
    ages = [
        user["age"]
        for user in users
        if isinstance(user.get("age"), (int, float))
        and not isinstance(user.get("age"), bool)
    ]
    return sum(ages) / len(ages) if ages else 0.0


def get_active_user_emails(users):
    """Return email addresses belonging to active users."""
    return [
        user["email"]
        for user in users
        if user.get("is_active") and "email" in user
    ]
