// Event firing should be enabled in backend/app/App.py in function do() for this to happen

var events = require('events');
var eventEmitter = new events.EventEmitter();

var myEventHandler1 = function () {
  console.log('Server send an update event! myEventHandler1 called');
}

var myEventHandler2 = function () {
  console.log('Server send an update event! myEventHandler2 called');
}

eventEmitter.on('server_update_event', myEventHandler1);
eventEmitter.on('server_update_event', myEventHandler2);