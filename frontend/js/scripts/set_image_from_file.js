last_filepath = ""

function set_image_from_file(filepath) {
    main_image_imgAreaSelect.cancelSelection();
    client.invoke("load_image_from_file", filepath, (error, res) => {
        try {
            set_image_from_base64("main_image", res);
        } catch (error) {
            console.log(error);
            alert('Could not set image');
        }
    })
    last_filepath = filepath;
} 







































// console.log($("#main_image_container").width());
// сonsole.log($("#main_image_container").height());
// сonsole.log($("#main_image").width());
// сonsole.log($("#main_image").height());

/*if ($("#main_image").css('width') > $("#main_image").css('height')) {
    $("#main_image").css('width', "98%");
}
else {
    $("#main_image").css('height', "98%");   
}*/