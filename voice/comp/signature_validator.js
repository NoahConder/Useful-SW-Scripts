import express from 'express';
import { RestClient } from '@signalwire/compatibility-api';
import ngrok from 'ngrok';

const app = express();

let url // Ngrok url

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.post("/", (req, res) => {
    const signingKey = "signature_key_here"; // signing key copied from your credentials page
    const signatureHeader = req.headers["x-signalwire-signature"];
    const requestURL = req.body.requestURL || `${url}/`;
    const requestBody = req.body;

    const valid = RestClient.validateRequest(signingKey, signatureHeader, requestURL, requestBody);

    if (valid) {
        console.log("Request signature is valid:");
        console.log("Signature Header:", signatureHeader);
        console.log("Request URL:", requestURL);
        console.log("Request Body:", requestBody);
        console.log("Validation Result:", valid);
        res.send("Request signature is valid.");
    } else {
        console.log("Request signature is invalid:");
        console.log("Signature Header:", signatureHeader);
        console.log("Request URL:", requestURL);
        console.log("Request Body:", requestBody);
        console.log("Validation Result:", valid);
        res.send("Request signature is invalid.");
    }
});

app.listen(8080, "0.0.0.0", async () => {
    url = await ngrok.connect(8080);
    console.log(`Server is hosted at: ${url}/`);
});