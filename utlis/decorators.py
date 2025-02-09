from functools import wraps
from time import time
from .storage import AUTHORIZED_USERS, rate_limit_dict
from config import TIME_WINDOW, MAX_MESSAGES

def auth_required(func):
    @wraps(func)
    def wrapper(message, *args, **kwargs):
        if message.from_user.id not in AUTHORIZED_USERS:
            return
        return func(message, *args, **kwargs)
    return wrapper

def check_rate_limit(user_id):
    current_time = time()
    user_times = rate_limit_dict[user_id]
    user_times = [t for t in user_times if current_time - t < TIME_WINDOW]
    rate_limit_dict[user_id] = user_times
    user_times.append(current_time)
    return len(user_times) <= MAX_MESSAGES 