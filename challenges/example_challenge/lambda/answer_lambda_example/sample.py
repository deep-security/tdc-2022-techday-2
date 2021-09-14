def handler(event, context):
    # Do all cool validation
    validation = "Something cool."
    if (validation != "Really specific answer"):
        raise Exception("You haven't finished, because...")
        return(False)
    return(True)