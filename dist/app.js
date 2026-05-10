import * as https from 'node:https';
import * as fs from 'node:fs';
import pkg from 'pg';
const { Client } = pkg;
//make sure you run npm install --save-dev @types/node @types/pg
/*
* Backend of server in charge of connecting
* to pgClient and servicing GET and POST
* requests
*/
//Certificate
//PEM password is: -------------
const sslOptions = {
    key: fs.readFileSync('key.pem'),
    cert: fs.readFileSync('certificate.pem')
};
//Error function used twice function serving html pages and
//post requests.
const getErrorMessage = (error) => {
    if (error instanceof Error)
        return error.stack ?? error.message;
    return String(error);
};
//Setup Database and Connect
const port = Number(process.env.PORT) || 8080;
const pgClient = new Client({
    connectionString: process.env.DATABASE_URL || 'postgresql://postgres:password@localhost:5432/VoiceBank',
    ssl: process.env.DATABASE_URL ? { rejectUnauthorized: false } : false
});
try {
    await pgClient.connect();
    console.log('Connected to PostgreSQL');
}
catch (err) {
    console.error('Connection to PostgreSQL failed:', err.stack);
}
//Create Server for Website
const server = https.createServer(sslOptions, (req, res) => {
    const pathname = new URL(req.url ?? '/', `https://${req.headers.host}`).pathname;
    // Function to serve html files
    const serveFile = (filePath, contentType) => {
        fs.readFile(filePath, (err, data) => {
            if (err) {
                console.error(err.stack);
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('500 Internal Server Error');
            }
            else {
                res.writeHead(200, { 'Content-Type': contentType });
                res.end(data);
            }
        });
    };
    //Get requests for website pages
    if (req.method === 'GET') {
        //Homepage
        if (pathname === '/') {
            serveFile('./index.html', 'text/html; charset=utf-8');
        }
        // Uncomment to allow viewing the css in browser
        else if (pathname === '/initialPrototype.css') {
            serveFile('./initialPrototype.css', 'text/css');
        } //Uncomment to allow viewing the js in browser
        else if (pathname === '/initialPrototype.js') {
            serveFile('./initialPrototype.js', 'application/javascript');
        }
        else {
            res.writeHead(404, { 'Content-Type': 'text/plain' });
            res.end('404 page not found');
        }
        //Post requests for website pages
        //Called by a user performing on click in 
    }
    else if (req.method === 'POST' && pathname === '/submituser') {
        let body = '';
        console.log("Within submituser");
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', async () => {
            try {
                const data = JSON.parse(body);
                //console.log("First Name: "+data);
                //console.log("Last Name: "+data);
                await pgClient.query('INSERT INTO users (firstname, lastname) VALUES ($1, $2)', [data[0], data[1]]);
                res.writeHead(200, { 'Content-Type': 'text/plain' });
                res.end('Data successfully submitted');
            }
            catch (error) {
                console.error(getErrorMessage(error));
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('500 Internal Server Error');
            }
        });
        //Called by initialPrototype.js's submitToDB() after a onClick event on the submit_btn
        //initialPrototype.js Converts all letters to lowercase and only allows numerical numbers
        //and a-z/A-Z characters.
    }
    else if (req.method === 'POST' && pathname === '/submitrecording') {
        let body = '';
        //Convert chunk to string array with pID and the audio 	
        req.on('data', chunk => {
            body += chunk.toString();
        });
        req.on('end', async () => {
            try {
                const data = JSON.parse(body);
                const pID = data[0];
                await pgClient.query('insert into recordings (p_id, recording) values ($1, $2)', [pID, data[1]]
                //'insert into recordings (user_id, recording) values ($1, CAST(\'1\' AS bytea))', [user_id]
                );
                res.writeHead(200, { 'Content-Type': 'text/plain' });
                res.end('data succesfully submitted');
            }
            catch (error) {
                console.error(getErrorMessage(error));
                res.writeHead(500, { 'Content-Type': 'text/plain' });
                res.end('500 Internal Server Error');
            }
        });
    }
    else {
        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('404 page not found');
    }
});
//Port is 8080
server.listen(port, () => {
    console.log(`Server running on port ${port}/`);
});
//# sourceMappingURL=app.js.map