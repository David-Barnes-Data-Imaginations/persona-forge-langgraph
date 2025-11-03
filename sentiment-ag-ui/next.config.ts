import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  experimental: {
    serverComponentsExternalPackages: [
      'fast-xml-parser',
      '@aws-sdk/xml-builder',
      '@langchain/aws',
    ],
  },
  // Add rewrites to handle relative paths for VAD model files
  async rewrites() {
    return [
      {
        source: '/:path*/silero_vad_legacy.onnx',
        destination: '/silero_vad_legacy.onnx',
      },
      {
        source: '/:path*/vad.worklet.bundle.min.js',
        destination: '/vad.worklet.bundle.min.js',
      },
      {
        source: '/:path*/ort-wasm.wasm',
        destination: '/ort-wasm.wasm',
      },
      {
        source: '/:path*/ort-wasm-simd.wasm',
        destination: '/ort-wasm-simd.wasm',
      },
    ];
  },
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
