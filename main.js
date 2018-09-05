const electron = require('electron')
const app = electron.app
const BrowserWindow = electron.BrowserWindow
const path = require('path')

//const index_html_path = 'frontend/html/'
const index_html_path = ''

/*************************************************************
 * py process
 *************************************************************/

const PY_DIST_FOLDER = 'backenddist'
const PY_FOLDER = 'backend'
const PY_MODULE = 'main' // without .py suffix

let pyProc = null
let pyPort = null

const guessPackaged = () => {
  const fullPath = path.join(__dirname, PY_DIST_FOLDER)
  return require('fs').existsSync(fullPath)
}

const getScriptPath = () => {
  if (!guessPackaged()) {
    return path.join(__dirname, PY_FOLDER, PY_MODULE + '.py')
  }
  if (process.platform === 'win32') {
    return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE + '.exe')
  }
  return path.join(__dirname, PY_DIST_FOLDER, PY_MODULE, PY_MODULE)
}

const selectPort = () => {
  pyPort = 4242
  return pyPort
}

const createPyProc = () => {
  let script = getScriptPath()
  let port = '' + selectPort()

  if (guessPackaged()) {
    pyProc = require('child_process').execFile(script, [port])
  } else {
    pyProc = require('child_process').spawn('python', [script, port], {shell: true, detached: true, stdio : "inherit"})
  }
 
  if (pyProc != null) {
    // console.log(pyProc)
    console.log('child process success on port ' + port)

  }
// pyProc.stdout.on('data', (data) => {
//   console.log(`child stdout:\n${data}`);
// });
// pyProc.stderr.on('data', (data) => {
//   console.error(`child stderr:\n${data}`);
// });
}

const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)


/*************************************************************
 * window management
 *************************************************************/

let mainWindow = null

const createWindow = () => {
  mainWindow = new BrowserWindow({width: 1024+256, height: 576, center: false, x:250, y: 250,
   resizable: true})
  mainWindow.loadURL(require('url').format({
    pathname: path.join(__dirname, index_html_path + 'index.html'),
    protocol: 'file:',
    slashes: true
  }))

  //
  //  CONSOLE
  //
  mainWindow.webContents.openDevTools()

  
  mainWindow.setMenu(null);

  mainWindow.on('closed', () => {
    mainWindow = null
  })
}

app.on('ready', createWindow)

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

app.on('activate', () => {
  if (mainWindow === null) {
    createWindow()
  }
})
