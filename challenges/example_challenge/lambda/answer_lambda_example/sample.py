def handler(event, context):
    # Do something really cool to verify if answer was achieved.
    validation = "Something cool."
    if (validation != "Really specific answer"):
        # Oh no, player didn't get it right!
        # Raise an exception and write the user a message.
        # Note: We currently don't show this message, but this might change in the future.
        raise Exception("You haven't finished it, because...")
        return(False)
    # If correct answer was achieved, you need to return True.
    return(True)