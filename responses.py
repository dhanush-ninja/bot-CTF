from random import choice, randint
import json



def get_response(user_input: str, message) -> str:
    """Generate a response based on the user input."""
    # if check_for_bad_words(user_input):
    #     return f"{message.author.mention} Please don't use bad words!"

    # Handle other cases, e.g., greetings
    if "hello" in user_input.lower():
        return f"Hello {message.author.mention}!"
    
    # Default response
    return "I'm not sure how to respond to that."