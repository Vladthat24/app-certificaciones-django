const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const { defineConfig } = require('@vue/cli-service')

module.exports = defineConfig({
  context: __dirname,
  entry: './src/main.js',
  output: {
    path: path.resolve('./assets/webpack_bundles/'),
    filename: "[name]-[hash].js"
  },
  plugins: [
    new BundleTracker({filename: './webpack-stats.json'})
  ],
})