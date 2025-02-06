from aiogram.fsm.state import State, StatesGroup

class SubscriptionStates(StatesGroup):
    waiting_for_topic = State()

class DigestStates(StatesGroup):
    waiting_for_period = State()

class AdminStates(StatesGroup):
    waiting_for_ban_details = State()
    waiting_for_user_id = State() 