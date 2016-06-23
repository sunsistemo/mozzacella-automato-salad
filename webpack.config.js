module.exports = {
    entry: {
        automato: "./salmonella/main.js"
    },
    output: {
        path: __dirname,
        filename: "[name].js",

        // export itself to a global var named "CA"
        libraryTarget: "var",
        library: "CA"
    },
    module: {
        loaders: [
            { test: /\.js$/, exclude: /node_modules/, loader: "babel-loader"},
            { test: /\.css$/, loader: "style!css" }
        ]
    }
};
