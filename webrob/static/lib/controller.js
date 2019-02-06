function OpenEASEController(webclientBaseURL) {

    var that = this;

    this.baseURL = webclientBaseURL;

    this.kbController = undefined;

    this.frameControl = undefined;

    this.menu = undefined;

    this.flask_user = undefined;

    this.clientFrame = undefined;

    this.setClientOptions = function (options) {
        that.clientOptions = options;
    };

    this.setPageControls = function (frameControl, menu, flask_user) {
        that.frameControl = frameControl;
        that.menu = menu;
        that.flask_user = flask_user;
    };

    this.setClientFrame = function (frame) {
        that.clientFrame = frame;
    };

    this.setKnowrobController = function (kbController) {
        that.kbController = kbController;
    };

    this.getOptions = function () {
        return that.clientOptions;
    };

    this.getFrameControl = function () {
        return that.frameControl;
    };

    this.getFlaskUser = function () {
        return that.flask_user;
    };


    this.switchClient = function(name) {
        $.getJSON(that.baseURL+'/'+name+'/webclient-description.json', '', function (response) {
            that.menu.update_webclient_interfaces(response["interfaces"]);
            var entryPageName = response["entrypage"];
            that.clientFrame.src = that.baseURL+'/'+name+'/'+entryPageName;
            $(that.clientFrame).load(function() {
                that.frameControl.setClientFrameWindow(that.clientFrame.contentWindow);
                that.frameControl.init(response["interfaces"]);
            })
        });
    };

    this.executeProlog = function (query, callback) {
        if(that.kbController !== undefined) {
            that.kbController.executeProlog(query, callback);
        }
    };

    this.setEpisode = function(category, episode) {
        if(that.kbController !== undefined) {
            that.kbController.setEpisode(category, episode);
        }
    };
}