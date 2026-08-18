def ask_user(question: str) -> str:
    """
    This function is used to ask the user a question when important information is missing.
    It takes a single argument, 'question', which is a string containing the question to be asked.
    The function returns the user's response as a string.
    """
    return input(question + "\nYour answer: ")