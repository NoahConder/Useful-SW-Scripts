import express from "express";
import { RestClient } from "@signalwire/compatibility-api";

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

const blocklist = ["+18156167816"];

app.post('/', (req, res) => {
    const response = new RestClient.LaML.VoiceResponse();
    const number = req.body.From;

    if (blocklist.includes(number)) {
        console.log("User on blocklist attempted to call. Denying call...")
        response.reject({ reason: "rejected" });
    } else {
        response.say('You are not on the blocklist. Goodbye.')
        response.hangup()
    }

    res.set("Content-Type", "text/xml");
    res.send(response.toString());
});

app.listen(8080, "0.0.0.0", () => {
    console.log("Server is hosted at: http://127.0.0.1:8080");
});
