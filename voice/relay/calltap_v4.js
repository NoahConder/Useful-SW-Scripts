import { SignalWire } from "@signalwire/realtime-api";

const client = await SignalWire({ project: "proj", token: "api-token" })

const voiceClient = client.voice;

// Listen for incoming calls
await voiceClient.listen({

    topics: ["office"],
    onCallReceived: async (call) => {
        console.log("Call received");
        // Answer the call
        await call.answer();

        // Start a tap
        const callTap = call.tapAudio({
            direction: "both",
            device: {
                type: "ws",
                uri: "wss://example.ngrok-free.app"
            },
            listen: {
                onStarted: () => {
                    console.log("Tap started");
                },
                onEnded: () => {
                    console.log("Tap ended");
                }
            }
        }).onStarted();
        await call.playTTS({ text: "We are currently tapping the call audio." });
        // Stop the tap
        await callTap.stop();
        call.hangup();
    }
});