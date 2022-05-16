const path = require('path');


module.exports = {
    mode: 'development',
    entry: "./frontend/main.js",
    output: {
        filename: `bundle.js`,
        path: path.resolve(__dirname, 'zorkweb/static')
    },
}