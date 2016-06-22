import { zfill, reverse, choice, range } from "./utils.js";


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

let r = 1;
let k = 2;
let ruleNum = 30;
let size = 80;
let rule = generateRule(r, k, ruleNum);
seedState(size, k);
printCA(r, rule);
