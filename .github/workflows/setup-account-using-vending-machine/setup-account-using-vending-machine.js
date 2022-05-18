const axios = require('axios').default;
const core = require('@actions/core');

const VM_ENDPOINT = process.env.VM_ENDPOINT || 'https://rmrs30pwai.execute-api.us-east-1.amazonaws.com/Dev/';
const VM_API_KEY = process.env.VM_API_KEY;
const CFN_URL = process.env.CFN_URL;
const MAX_WAIT_TIME_IN_MINUTES = process.env.MAX_WAIT_TIME_IN_MINUTES || 90;

const hoursToMillisec = (hours) => {
  return hours * 60 * 1000;
};

const expireTime = (hoursAfterRightNow) => {
  return Date.now() + hoursToMillisec(hoursAfterRightNow);
};

const setupRequest = (method, path, data) => {
  return {
    method: method,
    baseURL: VM_ENDPOINT,
    url: path,
    headers: {
      'x-api-key': VM_API_KEY,
      'Content-Type': 'application/json'
    },
    responseType: 'json',
    ...data && {data : data}
  };
};

const state = async (id) => {
  try {
    const resp = await axios(setupRequest('GET', `${id}/state`));
    return resp.data;
  }
  catch(err) {
    core.setFailed(err.message);
    throw err;
  }
};

const deploy = async (cfnUrl, hoursAfterRightNow) => {
  const data = {
      'template': cfnUrl,
      'numberOfAccounts': '1',
      'startTime': expireTime(hoursAfterRightNow).toString,
      'endTime': Date.now().toString
  };
  try {
    const resp = await axios(setupRequest('POST', 'create', data));
    return resp.data;
  }
  catch(err) {
    core.setFailed(err.message);
    throw err;
  }
};

const accounts = async (id) => {
  try {
    const resp = await axios(setupRequest('GET', `${id}/accounts`));
    return resp.data;
  }
  catch(err) {
    core.setFailed(err.message);
    throw err;
  }
};

const clean = async (id) => {
  try {
    const resp = await axios(setupRequest('DELETE', `${id}/clean`));
    return resp.data;
  }
  catch(err) {
    core.setFailed(err.message);
    throw err;
  }
};

const parseOutputs = (stackoutput) => {
  try {
    return stackoutput.reduce((outputs, pair) => {
      const key = pair.OutputKey;
      const value = pair.OutputValue;
      outputs[pair.OutputKey] = pair.OutputValue;
      return outputs;
    }, {});
  } catch (err) {
    core.setFailed(err.message);
  }
}

const sleep = async (ms) => {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
};


exports.handler = async () => {
  try {
    console.info(`Deploying ${CFN_URL} to Vending Machine...`);
    const id = (await deploy(CFN_URL, 1)).Id;
    console.info(`Deploy requested. Id is ${id}`);
    let waitedTimeInMinutes = 0;
    while ( (await state(id)).status != 'completed' ){
      console.info(`
Account not ready... waiting 1 minute and trying again.
For troubleshooting purposes, the deployment id is: ${id}
      `);
      await sleep(60000);
      waitedTimeInMinutes =+ 1;
      if (waitedTimeInMinutes >= MAX_WAIT_TIME_IN_MINUTES) {
        // Account hasn't finished building in time.
        const accountNotReadyErr = new Error(`
It looks like something went wrong...
Here's the info that we have:
${JSON.stringify((await accounts(id)), null, 2)}`));
        core.setFailed(accountNotReadyErr.message);
        throw accountNotReadyErr;
      }
    }

    console.info('Account is ready!\n');
    console.info('The outputs are:');
    return JSON.stringify(parseOutputs((await accounts(id))[0].stackoutput), null, 2);
  }
  catch(err) {
    core.setFailed(err.message);
    throw err;
  }

};

console.info(VM_ENDPOINT);
console.info(VM_API_KEY);
// const id = '0771612c-b23f-4cfb-ba14-e5c1050024d9';
// state(id)
exports.handler()
  .then(res => {
    console.log(res);
    return 0;
  })
  .catch(err => {
    console.error(err);
    core.setFailed(err.message);
    return -1;
  });
