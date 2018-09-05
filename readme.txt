This program performs some simple image processing tasks (based on electron-python-template repo).


Old readme from the template
-----------------------------
This is a demonstration of how you can make your own python-backend + js-frontend app.

You can run programm by executing 
./node_modules/.bin/electron .
If there are any errors, or you are launching it for the first time, consider running
./0_reinstall_electron.sh

Original work was made by this man: https://github.com/fyears/electron-python-example
but I've decided to change his code in some way, also simplifying, and sorting it into folders
to maintain project readability.
The first change: original post's backend hadn't it's own state and therefore could not do any work
without the frontend's demand. Mine has one, and your App class runs in it's own thread.
The second change: now backend has a client to message some events to the frontend.

If you want to make a cross-platform programm, that uses all the fancy things of js/html/css
and runs powerfull python (actually you can choose any language) backend, that can handle work
without frontend's explicit demand, you will find this template helpful.

Daniel Lotkov, 2018
entrolab@gmail.com