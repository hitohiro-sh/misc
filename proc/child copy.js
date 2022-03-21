const process = require('process');
const stdin = process.stdin

stdin.setEncoding('utf8');


console.log('child:Hello!')

stdin.on('data', (data) => {
    console.log('child:' + data)
});

process.on('message', (msg) => {
    console.log(msg);
});

stdin.on('end', () => {
    console.log('child:Finish!')
});