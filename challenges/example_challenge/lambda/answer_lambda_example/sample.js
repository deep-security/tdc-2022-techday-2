exports.handler = async (event, context) => {
  // Do something really cool to verify if answer was achieved.
  const succeed = true;
  if (succeed){
      // If correct answer was achieved, you need to return a successful context.
      // Also, you might want to add a message for the player.
      // This message isn't showed to the player today, but we might change this
      // behavior in the future.
      context.succeed('succeed is true');
  }
  else {
      // Oh no, player didn't get it right!
      // Fail the context and write the user a message.
      // Note: We currently don't show this message, but this might change in the future.
      context.fail('succeed is false');
  }
  return;
};
