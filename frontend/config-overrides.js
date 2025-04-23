const webpack = require('webpack');

module.exports = function override(config, env) {
    config.resolve.extensions = [...config.resolve.extensions, ".ts", ".js"]
    config.resolve.fallback = {
        'process/browser': require.resolve('process/browser'),
        path: require.resolve("path-browserify"),
        fs: require.resolve("browserify-fs"),
        stream: require.resolve("stream-browserify"),
        buffer: require.resolve("buffer"),
        util: false
    }

    config.plugins.push(
        new webpack.ProvidePlugin({
            Buffer: ["buffer", "Buffer"],
            process: "process/browser",
        }),
    );
    config.alias

    return config
}