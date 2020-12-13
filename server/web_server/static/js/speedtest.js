var Speedtest = function () {
    var self = this;

    // Fields
    var _request = new XMLHttpRequest();
    var _timeout = null;
    var _prevSpeedTime = null;
    var _prevLoadedBytes = 0;
    var _averageResults = [];

    // Properties
    self.Async = true;
    self.MovingAverage = 0;
    self.Timeout = 15;

    /*
        var speedtest = new Speedtest();
        speedtest.Ping("/", function (ms) {
            console.log(ms.toFixed(0));
        });
    */
    self.Ping = function (url, callback) {
        Reset();

        // Local
        var startTime = new Date();
        var noCache = "?t=" + new Date().getTime();

        _request.onloadend = function() {
            var ms = new Date() - startTime;
            callback(ms);
        };

        // Do request
        _request.open("HEAD", url + noCache, self.Async);
        _request.send(null);
    };

    /*
        var speedtest = new Speedtest();
        speedtest.Download("/20MB.zip", function (Mbps, data, done) {
            if (!done)
                console.log("Download: " + Mbps.toFixed(2) + " Mbps");
            else
                console.log("Download complete");
        });
    */
    self.Download = function (url, callback) {
        Reset();

        // Local
        var data = null;
        var speed = 0;
        var noCache = "?t=" + new Date().getTime();

        _request.onloadend = function() { callback(speed, data, true); };
        _request.onprogress = function(event) {
            // Has loaded bytes
            if (event.lengthComputable) {
                speed = Speed(event);
                data = this.response;
                callback(speed, data, false);
            }
        };
        
        // Do request
        _request.open("GET", url + noCache, self.Async);
        _request.send(null);
    };

    /*
        var speedtest = new Speedtest();
        speedtest.Upload("/upload", function (Mbps, done) {
            if (!done)
                console.log("Upload: " + Mbps.toFixed(2) + " Mbps");
            else
                console.log("Upload complete");
        });
   */
   self.Upload = function (url, data, callback) {
        Reset();

        // Local
        var speed = 0;
        _request.onloadend = function() { callback(speed, true); };
        _request.upload.onprogress = function(event) {
            // Has loaded bytes
            if (event.lengthComputable) {
                speed = Speed(event);
                callback(speed, false);
            }
        };

        // Do request
        _request.open("POST", url, self.Async);
        _request.send(data);
    };
    
    // Speed
    function Speed(event) {
        // Make sure not null
        if (_prevSpeedTime == null)
            _prevSpeedTime = new Date();

        // Calculate size
        var b = (event.loaded - _prevLoadedBytes) * 8;
        var Kb = b / 1024;
        var Mb = Kb / 1024;
        // Calculate speed
        var s = (new Date() - _prevSpeedTime) / 1000;
        var speed = Mb / s;

        // Set old values to new values
        _prevSpeedTime = new Date();
        _prevLoadedBytes = event.loaded;

        // Return average
        return Average(speed);
    }

    // Average
    function Average(result) {
        // Check if result number
        if (result > 0 && isFinite(result)) {
            // Moving average
            var avgCount = self.MovingAverage;
            if (avgCount > 0 && _averageResults.length > avgCount)
                _averageResults.splice(avgCount, _averageResults.length - avgCount - 1);

            // Append result
            _averageResults.push(result);

            //Return average of results
            return (_averageResults.reduce((a, b) => a + b, 0) / _averageResults.length);
        }
        // Nothing
        return 0;
    }

    // Timeout
    function Timeout() {
        _request.abort();
    }

    // Reset
    function Reset() {
        // Clear timeout
        if (_timeout != null)
            clearTimeout(_timeout);

        // Reset field values
        _prevSpeedTime = null;
        _prevLoadedBytes = 0;
        _averageResults = [];

        // Set timeout
        _timeout = setTimeout(Timeout, self.Timeout * 1000);
    }
};
