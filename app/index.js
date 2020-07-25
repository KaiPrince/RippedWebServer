import { Elm } from "./src/Main";

async function elmInit() {
  // Extract the stored data from previous sessions.
  var storedData = await browser.storage.sync.get();
  var flags = storedData || null;

  // Load the Elm app, passing in the stored data.
  var app = Elm.Main.init({
    node: document.getElementById("myapp"),
    flags: flags,
  });

  // Listen for commands from the `setStorage` port.
  // Turn the data to a string and put it in localStorage.
  app.ports.setStorage.subscribe(function (state) {
    browser.storage.sync.set(state);
  });
}

elmInit();
