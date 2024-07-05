import { Voice } from "@signalwire/realtime-api";
import dotenv from "dotenv";

dotenv.config();

const client = new Voice.Client({
    project: process.env.PROJECT,
    token: process.env.TOKEN,
    space: process.env.SPACE
});

async function dialer(client, from, to, url) {
    try {
        console.log("Dialing out...");
        const call = await client.calling.dialSip({
            from: from,
            to: to,
            timeout: 30.0
        });

        console.log("Call connected...");

        try {
            console.log("Transferring call to Call Flow Builder / SWML...");
            await client.execute({
                method: "calling.transfer",
                params: {
                    node_id: call.nodeId,
                    call_id: call.callId,
                    dest: url
                }
            });

            console.log("Call transferred successfully to Call Flow Builder or SWML bin.");
        } catch (error) {
            console.error("Error transferring call:", error);
            console.log("Hanging up call...");
            await call.hangup();
        }
    } catch (error) {
        console.error("Error making call:", error);
    } finally {
        process.exit(0); // Exit the script after handling the call
    }
}

// Example usage:
dialer(
    client,
    "+1555555555", // Replace with your SignalWire phone number/endpoint
    "sip:user@your-space-7c08b602ff5e.sip.signalwire.com", // Replace with the SIP endpoint or number you want to dial
    "your-swml-bin/call-flow-builder-link" // Replace with your Call Flow Builder (CFB) or SWML link
    // Note: you will need to add the version of the CFB script. See below for an example.
    // "https://example-space.signalwire.com/relay-bins/aeb49978-faea-414a-88dc-ba2b7e14b3a9?version=current_deployed"
);

