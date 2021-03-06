const process = require('process');
const stdin = process.stdin
const child_proccess = require('child_process');


stdin.setEncoding('utf8');


console.log('Hello!')

const child = child_proccess.spawn(process.argv[0], ['child.js'], {
    stdio: ['pipe', 1, 'pipe']
});

const child2 = child_proccess.spawn('go', ['run', 'child_proc.go'], {
    stdio: ['pipe', 1, 'pipe']
});

stdin.on('data', (data) => {
    
    console.log(data);

    let buf = JSON.stringify({ attr: data })
    child.stdin.write(buf);
    // console.log(buf)
    child2.stdin.write(`${buf}\n`);


});

stdin.on('end', () => {
    console.log('Finish!')
});
