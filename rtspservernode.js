//import RtspServer from 'rtsp-streaming-server'
const RtspServer = require('rtsp-streaming-server').default;

const server = new RtspServer({
    serverPort: 5554,
    clientPort: 6554,
    rtpPortStart: 10000,
    rtpPortCount: 10000
});
 
 
async function run() {
    try {
        await server.start();
    } catch (e) {
        console.error(e);
    }
}
 
run();