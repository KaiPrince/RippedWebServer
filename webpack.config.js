const path = require("path");

module.exports = {
  entry: { index: "./app/index.js" },
  mode: "production",
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "server/web_server/static/dist"),
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
              cwd: path.resolve(__dirname, "./app"),
              optimize: true,
            },
          },
        ],
      },
    ],
  },
};
