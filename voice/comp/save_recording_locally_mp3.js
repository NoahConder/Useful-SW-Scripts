import express from "express";
import { RestClient } from "@signalwire/compatibility-api";
import axios from 'axios';
import fs from 'fs';

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.json());


app.post("/", (req, res) => {
    const response = new RestClient.LaML.VoiceResponse();
    response.say("The agent is currently unavailable, please leave a message.");
    response.record({action: "/hangup",});
    res.set("Content-Type", "text/xml");
    res.send(response.toString());
});

app.post("/hangup", async (req, res) => {
    if (req.body.RecordingUrl) {
        let recordingUrl = req.body.RecordingUrl;
        console.log("Original Recording Url:", recordingUrl);

        // Sleep for 1 second.
        // The purpose of the sleep is to allow the MP3 file to be ready as the original file is a .wav and the MP3 is generated after.
        // Attempting to pull it too early will result in a 403 forbidden.
        await sleep(1000);

        // Replace .wav with .mp3 in the URL
        recordingUrl = recordingUrl.replace('.wav', '.mp3');
        const fileName = recordingUrl.split('/').pop();

        try {
            const response = await axios.get(recordingUrl, { responseType: "stream" });
            response.data.pipe(fs.createWriteStream(fileName));
            console.log("Recording saved as:", fileName);
        } catch (error) {
            if (error.response) {
                console.error("Error saving recording:", error.response.status, error.response.statusText);
            } else {
                console.error("Error saving recording:", error.message);
            }
        }
    }

    const voiceResponse = new RestClient.LaML.VoiceResponse();
    voiceResponse.hangup();
    res.set("Content-Type", "text/xml");
    res.send(voiceResponse.toString());
});

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

app.listen(8080, "0.0.0.0");
console.log("Server is hosted at: http://127.0.0.1:8080");
