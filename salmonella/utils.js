let leftPad = require("left-pad");


// left fill with zero's
export function zfill(s, width) {
    return leftPad(s, width, '0');
}

// string reversal
export function reverse(s) {
    return [...s].reverse().join("");
}

// generates random integers n: a <= n < b
export function randint(a, b) {
    return a + Math.floor(Math.random() * (b - a));
}

// choose uniform element from an array
export function choice(s) {
    return s[randint(0, s.length)];
}

export function range(a, b) {
    if (!b) {
        b = a;
        a = 0;
    }
    let x = Array(b - a);
    for (let i = 0; i < b - a; i++) {
        x[i] = a + i;
    }
    return x;
}
