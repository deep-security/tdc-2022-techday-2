var fs = require("fs");

// using the readFileSync() function
// and passing the path to the file
const buffer = fs.readFileSync("index.html");

// use the toString() method to convert
// Buffer into String
const html = buffer.toString();

exports.handler = async (event) => {
  const response = {
    statusCode: 200,
    headers: {
      "Content-Type": "text/html",
    },
    body: html,
  };
  return response;
};
