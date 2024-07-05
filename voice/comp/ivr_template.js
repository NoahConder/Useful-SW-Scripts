import express from "express";
import { RestClient } from "@signalwire/compatibility-api";

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());

// Prevents the IVR from being looped forever.
let count = 1;

app.post("/", (req, res) => {
    const response = new RestClient.LaML.VoiceResponse();
    const gather = response.gather({ input: "speech dtmf", timeout: 5, numDigits: 1, action: "/process" });
    gather.say("Thank you for calling IVR Test. Please say or press 1 for Support, 2 for sales or press 3 for hours of operation.");
    res.set("Content-Type", "text/xml");
    res.send(response.toString());
});

app.post("/process", (req, res) => {
    const response = new RestClient.LaML.VoiceResponse();
    console.log("Current loop count:", count);
    if (count === 3) {
        console.log("Looping. Hanging up...");
        response.hangup();
        count = 1; // Reset count
        res.set("Content-Type", "text/xml");
        res.send(response.toString());
    } else {
        console.log("User's selection:", req.body.Digits);
        if (req.body.Digits === "1") {
            response.say("Connecting you to support. This call will be recorded for quality purposes.");
            response.redirect("/support");
            count = 1; // Reset count on valid input

        } else if (req.body.Digits === "2") {
            response.say("Connecting you to sales. This call will be recorded for quality purposes.");
            response.redirect("/sales");
            count = 1; // Reset count on valid input

        } else if (req.body.Digits === "3") {
            response.say("Our current hours are 9AM to 5PM Monday through Friday.");
            count = 1; // Reset count on valid input

        } else {
            response.say("Sorry, I didn't understand that.");
            count++;
            response.redirect("/");
        }
        res.set("Content-Type", "text/xml");
        res.send(response.toString());
    }
});

app.post("/status", (req, res) => {
    console.log(req.body);
    res.sendStatus(200); // Send a response to avoid hanging the request
});

app.post("/support", (req, res) => {
    console.log(req.body);
    const response = new RestClient.LaML.VoiceResponse();
    let dial = response.dial({
        record: "record-from-ringing",
        recordingStatusCallback: "/status",
    });
    dial.number("+1553035050");
    res.set("Content-Type", "text/xml");
    res.send(response.toString());
});

app.post("/sales", (req, res) => {
    console.log(req.body);
    const response = new RestClient.LaML.VoiceResponse();
    let dial = response.dial({
        record: "record-from-ringing",
        recordingStatusCallback: "/status",
    });
    dial.sip("sip:example@example-space-55555555555.sip.signalwire.com");
    res.set("Content-Type", "text/xml");
    res.send(response.toString());
});

app.listen(8080, "0.0.0.0", () => {
    console.log("Server is hosted at: http://127.0.0.1:8080");
});
