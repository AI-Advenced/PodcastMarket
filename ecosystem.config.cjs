module.exports = {
  apps: [
    {
      name: 'podcastmarket',
      script: 'run.py',
      interpreter: 'python3',
      env: {
        FLASK_APP: 'run.py',
        FLASK_ENV: 'development',
        PORT: 3000
      },
      watch: false,
      instances: 1,
      exec_mode: 'fork',
      autorestart: true,
      max_restarts: 10,
      min_uptime: '10s'
    }
  ]
}
