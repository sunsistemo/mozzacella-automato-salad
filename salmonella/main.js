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

let r = 1;
let k = 2;
let ruleNum = 30;
let dx = 10;
let rule = generateRule(r, k, ruleNum);

let size = Math.floor(canvas.width / dx);
let ca = Array(Math.floor(canvas.height / dx));

let running = [];               // id's of the running CA's (ruleNum + timestamp as string)


function init_ca(ca) {
    ca[0] = STATE;
    for (let j = 1; j < ca.length; j++) {
        step(rule, r);
        ca[j] = STATE;
    }
    return ca;
}

function draw_ca(ctx, ca, id) {
    let size = Math.round(dx * 0.9);
    for (let j = 0; j < ca.length; j++) {
        for (let i = 0; i < STATE.length; i++) {
            if (ca[j][i] == '1') {
                ctx.fillStyle = "rgba(0, 0, 0, 1.0)";
                ctx.fillRect (i * dx, j * dx, size, size);
            } else {
                ctx.fillStyle = "#e3e5e3";
                ctx.fillRect (i * dx, j * dx, size, size);
            }
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
    rule = generateRule(r, k, ruleNum);
    let id = ruleNum.toString() + String(new Date().getTime());
    running.push(id);
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
