const { app, shell } = require('electron');
const { spawn } = require('child_process');
const http = require('http');

function waitForServer(url, callback) {
  const interval = setInterval(() => {
    http.get(url, res => {
      if (res.statusCode === 200) {
        clearInterval(interval);
        callback();
      }
    }).on('error', () => {
      // Server not ready yet
    });
  }, 500);
}

function launchDevServer() {
  const dev = spawn('npm', ['run', 'dev'], {
    shell: true,
    stdio: 'inherit',
  });

  waitForServer('http://localhost:5173', () => {
    shell.openExternal('http://localhost:5173');
  });
}

app.whenReady().then(launchDevServer);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') app.quit();
});
