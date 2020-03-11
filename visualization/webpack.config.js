const path = require("path");
const HtmlWebpackPlugin = require("html-webpack-plugin");

module.exports = {
  entry: "./src/index.js",
  output: {
    path: path.resolve(__dirname, "dist"),
    filename: "bundle.[hash].js"
  },
  externals: {
    d3: "https://d3js.org/d3.v5.min.js"
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.resolve(__dirname, "template.html")
    })
  ]
};
