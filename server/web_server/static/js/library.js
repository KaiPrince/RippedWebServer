/*
 * Project Name: RippedWebServer
 * File Name: library.js
 * Programmer: Kai Prince
 * Date: Sat, Dec 12, 2020
 * Description: This file contains all custom functions for the app.
 */

const humanizeSize = (bytes) => {
  const inKB = Number(bytes) / 1000;
  const inMB = inKB / 1000;
  const inGB = inMB / 1000;

  const atLeastAGB = inGB >= 1;
  const atLeastAMB = inMB >= 1;
  const atLeastAKB = inKB >= 1;

  if (atLeastAGB) return inGB.toFixed(2) + " GB";
  else if (atLeastAMB) return inMB.toFixed(2) + " MB";
  else if (atLeastAKB) return inKB.toFixed(2) + " KB";
  else return bytes + " bytes";
};

const humanizeTime = (seconds) => {
  if (Number.isNaN(seconds) || !Number.isFinite(seconds)) return "unknown";

  const inMinutes = Number(seconds) / 60;
  const inHours = inMinutes / 60;

  const atLeastASecond = seconds >= 1;
  const atLeastAMinute = inMinutes >= 1;
  const atLeastAnHour = inHours >= 1;

  if (atLeastAnHour) return inHours.toFixed(2) + " hours";
  else if (atLeastAMinute) return inMinutes.toFixed(2) + " minutes";
  else if (atLeastASecond) return seconds.toFixed(2) + " seconds";
  else return "<1 second";
};

// Size should be given in 'bytes'
function generate_random_data(size) {
  return new Blob([new ArrayBuffer(size)], {
    type: "application/octet-stream",
  });
}

const runUploadSpeedTest = (updateCallback) => {
  var speedtest = new Speedtest();
  speedtest.Async = true;
  speedtest.MovingAverage = 0;
  speedtest.Timeout = 15; // Times out after 15 seconds

  // "http://httpbin.org/post";
  // "http://localhost:5003"
  // "http://rippedtoastserver.ddns.net";
  const baseURL = "http://rippedtoastserver.ddns.net";
  const speedTestURL = baseURL + "/storage/speedtest";

  // 1MB should be enough for a good sample.
  const sizeInBytes = 1 * 1000 * 1000; // 1MB
  uploadData = generate_random_data(sizeInBytes);
  speedtest.Upload(speedTestURL, uploadData, function (Mbps, done) {
    if (!done) console.log("Upload: " + Mbps.toFixed(2) + " Mbps");
    else console.log("Upload complete");

    updateCallback(Mbps, done);
  });
};

const runDownloadSpeedTest = (updateCallback) => {
  var speedtest = new Speedtest();
  speedtest.Async = true;
  speedtest.MovingAverage = 0;
  speedtest.Timeout = 15; // Times out after 15 seconds

  // "http://httpbin.org/post";
  // "http://localhost:5003"
  // "http://rippedtoastserver.ddns.net";
  const baseURL = "http://rippedtoastserver.ddns.net";
  const speedTestURL = baseURL + "/storage/speedtest";

  speedtest.Download(speedTestURL, function (Mbps, data, done) {
    if (!done) console.log("Download: " + Mbps.toFixed(2) + " Mbps");
    else console.log("Download complete");

    updateCallback(Mbps, done);
  });
};
