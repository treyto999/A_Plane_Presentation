// This file is required by the index.html file and will
// be executed in the renderer process for that window.
// No Node.js APIs are available in this process because
// `nodeIntegration` is turned off. Use `preload.js` to
// selectively enable features needed in the rendering
// process.



var el = document.getElementById("clickMe");
if (el.addEventListener)
    el.addEventListener("click", doFunction, false);
else if (el.attachEvent)
    el.attachEvent('onclick', doFunction);

function doFunction() {
  var ps1 = new window.shell({
    executionPolicy: 'Bypass',
    noProfile: true
  });
   
  ps1.addCommand('cd ~/Desktop/HackResearch/');
  ps1.addCommand('./env/Scripts/activate');
  ps1.addCommand('python classifier.py');
  ps1.invoke()
  .then(output => {
    console.log(output);
  })
  .catch(err => {
    console.log(err);
  });

  var ps2 = new window.shell({
    executionPolicy: 'Bypass',
    noProfile: true
  });
   
  ps2.addCommand('cd ~/Desktop/HackResearch/');
  ps2.addCommand('./env/Scripts/activate');
  ps2.addCommand('python meanshift.py');
  ps2.invoke()
  .then(output => {
    console.log(output);
  })
  .catch(err => {
    console.log(err);
  });
}