exports.handler = async (event, context) => {
  // Do something really cool to verify if answer was achieved.
  const succeed = true;
  if (succeed){
      context.succeed('succeed is true');
  }
  else {
      context.fail('succeed is false');
  }
  return;
};
