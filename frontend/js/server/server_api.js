const zerorpc = require("zerorpc")

let server = new zerorpc.Server({
    // Typical functions to use
    with_reply: function(arg, reply) {
        reply(null, 'You send: ' + arg);
        alert('with_reply');
    },
    empty: function(reply) {
        reply();
        alert('empty');
    },
    emit_event: function(reply) {
        reply();
        eventEmitter.emit('server_event');        
    },

    // Real example
    update_event: function(reply) {
        reply();
        eventEmitter.emit('server_update_event');        
    },

    //
    // API STARTS HERE
    //
    set_main_image_from_base64: function(image, reply){
        reply();
        console.log('set_main_image_from_base64');
        set_main_image_from_base64(image);
    }
});





















// set_image_from_server: function(arg, reply){
//     reply();
//     console.log('set_image_from_server');
//     set_image_from_server(arg);
// }