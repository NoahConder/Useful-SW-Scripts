const WebSocket = require('ws');
const express = require('express');
const app = express();

const wss = new WebSocket.Server({ noServer: true });

wss.on('connection', (ws) => {
    console.log('WebSocket connection established');

    ws.on('message', (message) => {
        console.log(message);
        ws.send(message);
    });

    ws.on('close', () => {
        console.log('WebSocket connection closed');
    });
});

const server = app.listen(8080, "0.0.0.0", () => {
    console.log("Server is hosted at: http://127.0.0.1:8080");
});

server.on('upgrade', (request, socket, head) => {
    wss.handleUpgrade(request, socket, head, (ws) => {
        wss.emit('connection', ws, request);
    });
});
