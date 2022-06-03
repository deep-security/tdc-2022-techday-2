import { getSignedUrl } from "@aws-sdk/s3-request-presigner";
import { PutObjectCommand, S3Client } from "@aws-sdk/client-s3";
import { formatUrl } from "@aws-sdk/util-format-url";
import crypto from "crypto";
import { promisify } from "util";

const bucket = "alex-is-tired-quarantine";
const accessPoint = bucket;
const region = "us-west-1";

const credentials = {
  accessKeyId: process.env.AWS_ACCESS_KEY_ID || "",
  secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY || "",
};

const api_endpoint = process.env.API_ENDPOINT || "/";

const client = new S3Client({
  region: region,
  credentials: credentials,
});

async function generateUploadURL() {
  const randomBytes = promisify(crypto.randomBytes);
  const rawBytes = await randomBytes(16);
  const imageName = rawBytes.toString("hex");

  const putObjectCommand = new PutObjectCommand({
    Bucket: bucket,
    Key: imageName,
  });
  const putUrl = await getSignedUrl(client, putObjectCommand, {
    expiresIn: 3600,
  });
  return { putUrl, imageName };
}

// init
const imageForm = document.querySelector("#imageForm");
const imageInput = document.querySelector("#imageInput");

imageForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const file = imageInput.files[0];

  // get secure url from our server
  const { putUrl, imageName } = await generateUploadURL();
  console.log(putUrl);
  console.log(imageName);

  // post the image direclty to the s3 bucket
  await fetch(putUrl, {
    method: "PUT",
    body: file,
  });

  const getUrl = await fetch(
    `${api_endpoint}geturl/${imageName}`,
  ).then((response) => response.json());

  const img = document.createElement("img");
  img.src = await fetch(getUrl).then((response) => {
    if (response.status == 200) {
      return getUrl;
    } else {
      return `https://http.cat/${response.status}`;
    }
  });

  document.body.appendChild(img);
});
