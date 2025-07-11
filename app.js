#!/usr/bin/env node

// Plesk Node.js startup script
const { spawn } = require('child_process');
const path = require('path');

const projectRoot = __dirname;
const nextBin = path.join(projectRoot, 'node_modules', '.bin', 'next');

// Start Next.js in production mode
const nextProcess = spawn('node', [nextBin, 'start'], {
  cwd: projectRoot,
  stdio: 'inherit',
  env: {
    ...process.env,
    NODE_ENV: 'production',
    PORT: process.env.PORT || 3000,
  }
});

nextProcess.on('close', (code) => {
  console.log(`Next.js process exited with code ${code}`);
  process.exit(code);
});

nextProcess.on('error', (err) => {
  console.error('Failed to start Next.js process:', err);
  process.exit(1);
});

// Handle process termination
process.on('SIGINT', () => {
  console.log('Received SIGINT, terminating Next.js process...');
  nextProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  console.log('Received SIGTERM, terminating Next.js process...');
  nextProcess.kill('SIGTERM');
});

console.log('Aluplan Marketing List starting on port', process.env.PORT || 3000);
