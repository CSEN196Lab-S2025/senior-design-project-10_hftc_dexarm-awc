import { spawn } from 'child_process';
// import fetch from 'node-fetch';

// --- Configuration ---
// Define the URL of your Python Flask server endpoint
// Make sure the host and port match your running inference.py script
const serverUrl = 'http://127.0.0.1:2000/trigger-inference';


/************************************ RUN PYTHON FILES ************************************/

function runPythonScript(script, args = []) {
    return new Promise((resolve, reject) => {
        const child = spawn('python', ['-u', script, ...args], {
            stdio: 'inherit', // share stdout/stderr with Node's terminal
            env: { ...process.env, PYTHONUNBUFFERED: '1' }
        });

        child.on('close', (code) => {
            if (code !== 0) {
                reject(new Error(`Script ${script} exited with code ${code}`));
            } else {
                resolve();
            }
        });
    });
}



/************************************ QC ************************************/
// Function to send the trigger request to the server and handle the response
async function sendTriggerRequest() {
    console.log(`[INFO] Sending GET request to: ${serverUrl}`);

    try {
        // --- Send the GET request using fetch ---
        const response = await fetch(serverUrl, {
            method: 'GET', // Explicitly set method to GET
            headers: {
                'Accept': 'application/json' // Indicate we expect JSON back
            }
        });

        // --- Check if the response status is OK (e.g., 200-299) ---
        if (!response.ok) {
            // If response is not OK, log the status and try to get error text
            const errorText = await response.text(); // Get response body as text
            console.error(`[ERROR] Server responded with status: ${response.status} ${response.statusText}`);
            console.error(`[ERROR] Server response body: ${errorText}`);
            // Throw an error to be caught by the outer catch block
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        // --- Parse the JSON response ---
        // .json() parses the response body as JSON
        const jsonData = await response.json();

        // --- Print the received JSON data ---
        console.log('[INFO] Received JSON response from server:');
        // Use JSON.stringify with indentation for pretty printing
        console.log(JSON.stringify(jsonData, null, 2));

    } catch (error) {
        // --- Handle potential errors (network issues, JSON parsing errors, etc.) ---
        console.error('[ERROR] Failed to send trigger request or process response:');
        console.error(error); // Log the full error object
    }
}


/************************************  LASER CUTTER ************************************/
async function lasercut(isNameTag) {
    let args;
    if(isNameTag) 
        args = ['NameTagCutOut.gc']; // or change based on isNameTag if needed
    else
        args = ['signageTest.gc']; // or change based on isNameTag if needed

    await runPythonScript('lasercutter.py', args);
}

async function main() {
    const isNameTag = false;
    let count = 1; //number of item; increments at each item by 2

    try {
        await runPythonScript('phase1-lulu.py', [isNameTag?1:0]);
        await lasercut(isNameTag);
        await runPythonScript('phase2-lulu.py', [isNameTag?1:0]);

        // QUALITY CHECK
        setTimeout(() => {sendTriggerRequest()}, 5000);
    
        if (!isNameTag) {
            await runPythonScript('phase1-signage.py', [count]);
        } else {
            await runPythonScript('phase3-lulu.py', [isNameTag?1:0]);
            await runPythonScript('phase1-magneto.py');
        }

        console.log("Done?");
    } catch (err) {
        console.error("Script error:", err.message);
    }
}

setTimeout(() => {
    main();
}, 5000);