import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  serverExternalPackages: [
      'fast-xml-parser',
      '@aws-sdk/xml-builder',
      '@langchain/aws',
    ],
  webpack: (config, { isServer }) => {
    if (isServer) {
      config.externals = config.externals || [];
      config.externals.push({
        'fast-xml-parser': 'commonjs fast-xml-parser',
      });
    }
    
    // Handle .onnx and WASM files - copy to public directory
    config.module.rules.push({
      test: /\.onnx$/,
      type: 'asset/resource',
      generator: {
        filename: '[name][ext]',
        publicPath: '/',
      },
    });
    
    // Ignore node_modules for file watching to improve performance
    config.watchOptions = {
      ignored: /node_modules/,
    };
    
    return config;
  },
  // Ensure static files are served correctly
  assetPrefix: '',
  basePath: '',
};

export default nextConfig;
