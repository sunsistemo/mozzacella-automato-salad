import { zfill, reverse, choice, range, randint } from "./utils.js";


let STATE;

function generateRule(r, k, ruleNum) {
    let rule = {};
    let hood = 2 * r + 1;
    let bruleNum = reverse(zfill(ruleNum.toString(k), k ** hood));
    for (let s = 0; s < k ** hood; s++) {
        rule[zfill(s.toString(k), hood)] = parseInt(bruleNum[s]);
    }
    return rule;
}

function step(rule, r) {
    let oldState = STATE;
    let newState = Array(oldState.length);
    for (let n = 0; n < r; n++) {
        newState[n] = String(rule[oldState.slice(-r+n) + oldState.slice(0, r+n+1)]);
    }
    for (let i = r; i < oldState.length - r; i++) {
        newState[i] = String(rule[oldState.slice(i-r, i+r+1)]);
    }
    for (let m = 1; m < r + 1; m++) {
        newState[oldState.length - m] = String(rule[oldState.slice(-r-m) + oldState.slice(0, -m+r+1)]);
    }
    STATE = newState.join("");
}

function seedState(size, k) {
    let nums = range(k).map(String);
    STATE = range(size).map(() => choice(nums)).join("");
}

function randbit(rule, r) {
    step(rule, r);
    return parseInt(STATE[0]);
}

function printCA(r, rule) {
    console.log(STATE);
    step(rule, r);
    window.setTimeout(printCA, 100, r, rule);
}

let canvas = document.getElementById('1D_CA');
let ctx = canvas.getContext('2d');

let r, k, ruleNum, rule;
let random;                     // switch whether to pick a random rule or not

let dx = 10;
let size = Math.floor(canvas.width / dx);
let ca = Array(Math.floor(canvas.height / dx));

let running = [];               // id's of the running CA's (timestamp as string)


function init_ca(ca) {
    ca[0] = STATE;
    for (let j = 1; j < ca.length; j++) {
        step(rule, r);
        ca[j] = STATE;
    }
    return ca;
}

k = 2;
let styles;
function set_style(k) {
    // set the rectangle style (colour) for different number of states
    if (k == 2) {
        styles = {'0': "#e3e5e3",
                  '1': "rgba(0, 0, 0, 1.0)"};
    } else if (k == 3) {
        styles = {'0': "rgba(200, 0, 0, 1.0)",
                  '1': "rgba(0, 200, 0, 1.0)",
                  '2': "rgba(0, 0, 200, 1.0)"};
    } else if (k == 4) {
        styles = {'0': "#00BFFF",
                  '1': "#C000FF",
                  '2': "#FF4000",
                  '3': "#40FF00"};
    } else {                    // ehhhh...
        styles = {};
        for (let c of range(k)) {
            let x, y, z;
            [x, y, z] = [randint(0, 255).toString(), randint(0, 255).toString(), randint(0, 255).toString()];
            styles[String(c)] = "rgba(" + a + ',' + b + ',' + c + ')';
        }
    }
}
set_style(k);

function draw_ca(ctx, ca, id) {
    let size = Math.round(dx * 0.9);
    for (let j = 0; j < ca.length; j++) {
        for (let i = 0; i < STATE.length; i++) {
            ctx.fillStyle = styles[ca[j][i]];
            ctx.fillRect (i * dx, j * dx, size, size);
        }
    }

    let old_ca = ca;
    for (let j = 0; j < ca.length - 1; j++) {
        ca[j] = old_ca[j + 1];
    }
    step(rule, r);
    ca[ca.length - 1] = STATE;

    if (running.indexOf(id) > -1) {
        window.setTimeout(draw_ca, 200, ctx, ca, id);
    }
}

function start_1D_CA() {
    running.pop();
    let input_rule = document.getElementById("input_rule");
    ruleNum = parseInt(input_rule.value);
    let input_states = document.getElementById("input_states");
    k = parseInt(input_states.value);
    let input_neighbours = document.getElementById("input_neighbours");
    r = parseInt(input_neighbours.value);

    let input_random = document.getElementById("input_random");
    random = input_random.checked;
    if (random) {                                // pick a random rule
        let rules = (k ** (k ** (2 * r + 1)));   // number of possible rules
        ruleNum = randint(0, rules);
        input_rule.value = ruleNum.toString();
    }

    let id = String(new Date().getTime());
    running.push(id);
    rule = generateRule(r, k, ruleNum);
    set_style(k);
    seedState(size, k);
    init_ca(ca);
    draw_ca(ctx, ca, id);
}

function replace_CA() {
    running.pop();
    start_1D_CA();
}

function draw_single(ctx, t) {
    let dx = 20;
    let size = Math.round(dx * 0.78);
    if (t * dx >= canvas.height) {
        t = 0;
    }
    for (let i = 0; i < STATE.length; i++) {
        if (STATE[i] == '1') {
            ctx.fillStyle = "rgba(0, 0, 0, 1.0)";
            ctx.fillRect (i * dx, t * dx, size, size);
        } else {
            ctx.fillStyle = "#e3e5e3";
            ctx.fillRect (i * dx, t * dx, size, size);
        }
    }
    step(rule, r);
    window.setTimeout(draw_ca, 100, ctx, t + 1);
}


start_1D_CA();


module.exports = {
    "start_1D_CA": start_1D_CA
};
