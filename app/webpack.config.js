const path = require("path");

module.exports = {
  entry: { index: "./index.js" },
  mode: "production",
  output: {
    filename: "[name].js",
    path: path.resolve("/", "dist"), //path.resolve(__dirname, "dist"),
  },
  resolve: {
    extensions: [".elm", ".ts", ".js"],
  },
  module: {
    rules: [
      {
        test: /\.elm$/,
        exclude: [/elm-stuff/, /node_modules/],
        use: [
          { loader: "elm-hot-webpack-loader" },
          {
            loader: "elm-webpack-loader",
            options: {
              cwd: path.resolve(__dirname, "."),
              optimize: true,
            },
          },
        ],
      },
    ],
  },
  // Necessary for file changes inside the bind mount to get picked up
  watchOptions: {
    aggregateTimeout: 300,
    poll: 1000,
  },
};
