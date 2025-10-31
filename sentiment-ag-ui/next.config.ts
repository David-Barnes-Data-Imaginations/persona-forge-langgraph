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
  webpack: (config, { isServer }) => {
    if (isServer) {
      config.externals = config.externals || [];
      config.externals.push({
        'fast-xml-parser': 'commonjs fast-xml-parser',
      });
    }
    return config;
  },
};

export default nextConfig;
