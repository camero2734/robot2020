let A_Star = require("./a_star.js");
let genObstacles = require("./3Dobstacles.js");

// How many tests?
let runCount = 1000;



let start = {x: 36, y: 90};
let end = {x: 36, y: 10};

// Grid-erize numbers (i.e. 359.5 -> 108)
let five = (n) => Math.round(n/5);

function runAstar() {
    let obs = genObstacles();

    let startTime = Date.now();
    let p = A_Star(start, end, obs);

    return ((Date.now() - startTime) / 1000);
}

let sum = 0;
let max_val = 0;
console.log(`Running ${runCount} pathfinding attempts...`);
for (let i = 0; i < runCount; i++) {
    let time = runAstar();
    sum+=time;
    max_val = Math.max(time, max_val);
    console.log(`Run #${i+1} (${sum/(i+1)})`);
}
console.log(`Avg: ${sum/runCount}, Max: ${max_val},\nMax openSet len: ${maxOpenSetLength}`);
