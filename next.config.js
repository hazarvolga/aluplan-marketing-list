/** @type {import('next').NextConfig} */
const nextConfig = {
  // Production build optimizations
  output: 'standalone',
  
  // Plesk compatibility
  trailingSlash: true,
  
  // Asset optimization
  images: {
    unoptimized: true,
  },
  
  // Disable strict mode for production
  reactStrictMode: false,
  
  // API routes configuration
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: '/api/:path*',
      },
    ]
  },
  
  // Environment variables
  env: {
    CUSTOM_KEY: 'aluplan-marketing-list',
  },
  
  // Webpack configuration
  webpack: (config, { buildId, dev, isServer, defaultLoaders, webpack }) => {
    // Custom webpack config for Plesk
    return config
  },
  
  // Experimental features
  experimental: {
    // Enable for better performance
    optimizeCss: true,
  },
}

module.exports = nextConfig
