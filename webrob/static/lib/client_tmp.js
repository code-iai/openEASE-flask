/**
 * Establishes connection to a ROS master via websocket.
 **/
class KnowrobClient {

    constructor(options){
        this.options = options;

        this.that = this;
        // Object that holds user information
        this.flask_user = options.flask_user;
        // ROS handle
        this.ros = undefined;
        // URL for ROS server
        this.rosURL = options.ros_url || 'ws://localhost:9090';
        // Use rosauth?
        this.authentication  = options.authentication === '' ? true : options.authentication === 'True';
        // URL for rosauth token retrieval
        this.authURL  = options.auth_url || '/wsauth/v1.0/by_session';
        // The selected episode
        this.episode;
        // The openEASE menu that allows to activate episodes/ui/..
        this.menu = options.menu;
        // global jsonprolog handle
        this.prolog;

        // User interface names (e.g., editor, memory replay, ...)
        this.user_interfaces = options.user_interfaces || [];
        this.user_interfaces_flat = options.user_interfaces_flat || [];
        // Query parameters encoded in URL
        // E.g., localhost/#foo&bar=1 yields in:
        //    URL_QUERY = {foo: undefined, bar: 1}
        this.urlQuery = {};

        this.pageOverlayEnabled = false;
        // true iff connection to ROS master is established
        this.isConnected = false;
        // true iff json_prolog is connected
        this.isPrologConnected = false;
        // true iff registerNodes was called before
        this.isRegistered = false;
        // Prefix for mesh GET URL's
        this.meshPath  = options.meshPath || '/';
        // Block the interface until an episode was selected?
        this.requireEpisode = options.require_episode;
        // Viewer used by tutorial page
        this.globalViewer = options.global_viewer;

        // sprite markers and render events
        this.sprites = [];
        this.render_event;

        // The selected marker object or undefined
        this.selectedMarker = undefined;

        // ROS messages
        this.tfClient = undefined;
        this.markerArrayClient = undefined;
        this.designatorClient = undefined;
        this.imageClient = undefined;
        this.cameraPoseClient = undefined;
        this.snapshotTopic = undefined;

        this.nodesRegistered = false;

        // Redirects incomming marker messages to currently active canvas.
        function CanvasProxy() {
            this.viewer = function() {
                var ui = that.getActiveFrame().ui;
                if(!ui)
                    return undefined;
                if(!ui.rosViewer)
                    return undefined;
                return ui.rosViewer.rosViewer;
            };
            this.addMarker = function(marker,node) {
                if(this.viewer())
                    this.viewer().addMarker(marker,node);
            };
            this.removeMarker = function(marker,node) {
                if(this.viewer())
                    this.viewer().removeMarker(marker,node);
            };
        };
        this.canvas = new CanvasProxy();
    }

    init() {
        /*
        // Connect to ROS.
        that.connect();

        that.episode = new KnowrobEpisode(that);
        if(options.category && options.episode)
            that.episode.setEpisode(options.category, options.episode);

        that.createIOSPageOverlay;

        if(requireEpisode && !that.episode.hasEpisode()) {
          that.showPageOverlay("Please select an Episode");
        } else {
          that.showPageOverlay("Loading Knowledge Base");
        }

        setInterval(containerRefresh, 570000);
        containerRefresh();
        render_event = new CustomEvent('render', {'camera': null});
        */
    };

    containerRefresh() {
        $.ajax({
            url: '/api/v1.0/refresh_by_session',
            type: "GET",
            contentType: "application/json",
            dataType: "json"
        });
    };

    connect() {
        if(that.ros) return;
        that.ros = new ROSLIB.Ros({url : rosURL});
        that.ros.on('connection', function() {
            that.isConnected = true;
            console.log('Connected to websocket server.');
            if (authentication) {
                // Acquire auth token for current user and authenticate, then call registerNodes
                that.authenticate(authURL, that.registerNodes);
            } else {
                // No authentication requested, call registerNodes directly
                that.registerNodes();
                that.waitForJsonProlog();
            }
        });
        that.ros.on('close', function() {
            console.log('Connection was closed.');
            that.showPageOverlay("Connection was closed, reconnecting...");
            that.ros = undefined;
            that.isRegistered = false;
            setTimeout(that.connect, 500);
        });
        that.ros.on('error', function(error) {
            console.log('Error connecting to websocket server: ', error);
            that.showPageOverlay("Connection error, reconnecting...");
            if(that.ros) that.ros.close();
            that.ros = undefined;
            that.isRegistered = false;
            setTimeout(that.connect, 500);
        });
    };

    authenticate(authurl, then) {
        console.log("Acquiring auth token");
        // Call wsauth api to acquire auth token by existing user login session
        $.ajax({
            url: authurl,
            type: "GET",
            contentType: "application/json",
            dataType: "json"
        }).done( function (request) {
            if(!that.ros) {
                console.warn("Lost connection to ROS master.");
                return;
            }
            console.log("Sending auth token");
            that.ros.authenticate(request.mac,
                request.client,
                request.dest,
                request.rand,
                request.t,
                request.level,
                request.end);
            that.waitForJsonProlog();

            // If a callback function was specified, call it in the context of Knowrob class (that)
            if(then) {
                then.call(that);
            }
        });
    };

    registerNodes() {
        if(that.isRegistered) return;
        that.isRegistered = true;

        // Setup publisher that sends a dummy message in order to keep alive the socket connection
        {
            var interval = options.interval || 30000;
            // The topic dedicated to keep alive messages
            var keepAliveTopic = new ROSLIB.Topic({ ros : that.ros, name : '/keep_alive', messageType : 'std_msgs/Bool' });
            // A dummy message for the topic
            var keepAliveMsg = new ROSLIB.Message({ data : true });
            // Function that publishes the keep alive message
            var ping = function() { keepAliveTopic.publish(keepAliveMsg); };
            // Call ping at regular intervals.
            setInterval(ping, interval);
        };

        // topic used for publishing canvas snapshots
        that.snapshotTopic = new ROSLIB.Topic({
            ros : that.ros,
            name : '/openease/video/frame',
            messageType : 'sensor_msgs/Image'
        });

        // Setup a client to listen to TFs.
        this.tfClient = new ROSLIB.TFClient({
            ros : that.ros,
            angularThres : 0.01,
            transThres : 0.01,
            rate : 10.0,
            fixedFrame : '/my_frame'
        });

        // Setup the marker array client.
        that.markerArrayClient = new EASE.MarkerArrayClient({
            ros : that.ros,
            tfClient : tfClient,
            topic : '/visualization_marker_array',
            canvas : that.canvas,
            path : meshPath
        });

        // Setup the designator message client.
        designatorClient = new ROSLIB.Topic({
            ros : that.ros,
            name : '/logged_designators',
            messageType : 'designator_integration_msgs/Designator'
        });
        designatorClient.subscribe(function(message) {
            if(message.description.length==0) {
                console.warn("Ignoring empty designator.");
            }
            else {
                var desig_js = parse_designator(message.description);
                var html = format_designator(message.description);
                if(that.getActiveFrame().on_designator_received)
                    that.getActiveFrame().on_designator_received(html);
            }
        });

        // Setup the image message client.
        imageClient = new ROSLIB.Topic({
            ros : that.ros,
            name : '/logged_images',
            messageType : 'std_msgs/String'
        });
        imageClient.subscribe(function(message) {
            var ext = message.data.substr(message.data.lastIndexOf('.') + 1).toLowerCase();
            var url = message.data;
            if(!url.startsWith("/knowrob/")) {
                if(url.startsWith("/home/ros/user_data"))  url = '/user_data/'+url.replace("/home/ros/user_data/", "");
                else url = '/knowrob/knowrob_data/'+url;
            }
            var imageHeight, imageWidth;
            var html = '';
            if(ext=='jpg' || ext =='png') {
                html += '<div class="image_view">';
                html += '<img id="mjpeg_image" class="picture" src="'+url+'" width="300" height="240"/>';
                html += '</div>';

                imageHeight = function(mjpeg_image) { return mjpeg_image.height; };
                imageWidth  = function(mjpeg_image) { return mjpeg_image.width; };
            }
            else if(ext =='ogg' || ext =='ogv' || ext =='mp4' || ext =='mov') {
                html += '<div class="image_view">';
                html += '  <video id="mjpeg_image" controls autoplay loop>';
                html += '    <source src="'+url+'" ';
                if(ext =='ogg' || ext =='ogv') html += 'type="video/ogg" ';
                else if(ext =='mp4') html += 'type="video/mp4" ';
                html += '/>';
                html += 'Your browser does not support the video tag.';
                html += '</video></div>';

                imageHeight = function(mjpeg_image) { return mjpeg_image.videoHeight; };
                imageWidth  = function(mjpeg_image) { return mjpeg_image.videoWidth; };
            }
            else {
                console.warn("Unknown data format on /logged_images topic: " + message.data);
            }
            if(html.length>0 && that.getActiveFrame().on_image_received) {
                that.getActiveFrame().on_image_received(html, imageWidth, imageHeight);
            }
        });

        // TODO redo highlighting with dedicated messages
//       var highlightClient = new ROSLIB.Topic({
//         ros : that.ros,
//         name : '/ease/canvas/highlight',
//         messageType : 'std_msgs/String'
//       });
//       highlightClient.subscribe(function(message) {
//         var objectId = message.data;
//         console.info(objectId);
//         if(objectId == '*') {
//         } else {
//         }
//       });
//       var unhighlightClient = new ROSLIB.Topic({
//         ros : that.ros,
//         name : '/ease/canvas/unhighlight',
//         messageType : 'std_msgs/String'
//       });
//       highlightClient.subscribe(function(message) {
//         var objectId = message.data;
//         console.info(objectId);
//         if(objectId == '*') {
//         } else {
//         }
//       });

        cameraPoseClient = new ROSLIB.Topic({
            ros : that.ros,
            name : '/camera/pose',
            messageType : 'geometry_msgs/Pose'
        });
        cameraPoseClient.subscribe(function(message) {
            if(that.getActiveFrame().on_camera_pose_received)
                that.getActiveFrame().on_camera_pose_received(message);
        });

        // NOTE: frame windows may not be loaded already
        for(var i in user_interfaces) {
            var frame = document.getElementById(user_interfaces[i].id+"-frame");
            if(frame && frame.contentWindow && frame.contentWindow.on_register_nodes)
                frame.contentWindow.on_register_nodes();
        }
        that.nodesRegistered = true;
    };

    waitForJsonProlog() {
        var client = new JsonProlog(that.ros, {});
        client.jsonQuery("true", function(result) {
            client.finishClient();
            if(result.error) {
                // Service /json_prolog/simple_query does not exist
                setTimeout(that.waitForJsonProlog, 500);
            }
            else {
                that.hidePageOverlay();
                if(requireEpisode && !that.episode.hasEpisode())
                    that.showPageOverlay("Please select an Episode");
                that.isPrologConnected = true;
                that.episode.selectMongoDB();
            }
        });
    };

    ///////////////////////////////
    //////////// Marker Visualization
    ///////////////////////////////

    newProlog() {
        return that.ros ? new JsonProlog(that.ros, {}) : undefined;
    };

    newCanvas(options) {
        var x = new KnowrobCanvas(that, options);
        // connect to render event, dispatch to marker clients
        // FIXME TypeError: x.rosViewer.on is not a function
        //x.rosViewer.on('render', function(e) {
        //    if(that.markerClient)      that.markerClient.emit('render', e);
        //    if(that.markerArrayClient) that.markerArrayClient.emit('render', e);
        //});
        return x;
    };

    newDataVis(options) {
        return new DataVisClient(options);
    };

    newTaskTreeVis(options) {
        return new TaskTreeVisClient(options);
    };

    selectMarker(marker) {
        if(that.selectedMarker == marker)
            return;
        if(that.selectedMarker) {
            if(that.canvas.viewer()) {
                that.canvas.viewer().unhighlight(that.selectedMarker);
            }
        }
        that.selectedMarker = marker;
        // inform the active iframe about selection (e.g., to show object query library)
        if(that.getActiveFrame())
            that.getActiveFrame().selectMarker(marker);
        // tell the webgl canvas to highlight the selected object
        if(that.canvas.viewer())
            that.canvas.viewer().highlight(marker);
    };

    unselectMarker() {
        if(!that.selectedMarker)
            return;
        if(that.getActiveFrame() && that.getActiveFrame().unselectMarker)
            that.getActiveFrame().unselectMarker(that.selectedMarker);
        // tell the webgl canvas to unhighlight the object
        if(that.canvas.viewer())
            that.canvas.viewer().unhighlight(that.selectedMarker);
        that.selectedMarker = undefined;
    };

    removeMarker(marker) {
        if(marker === that.selectedMarker) {
            that.unselectMarker();
        }
        if(that.getActiveFrame() && that.getActiveFrame().removeMarker)
            that.getActiveFrame().removeMarker(marker);
    };

    showMarkerMenu(marker) {
        if(that.getActiveFrame() && that.getActiveFrame().showMarkerMenu)
            that.getActiveFrame().showMarkerMenu(marker);
    };

    on_render(camera,scene) {
        if(that.getActiveFrame() && that.getActiveFrame().on_render)
            that.getActiveFrame().on_render(camera,scene);

        var index;
        for(index = 0; index < sprites.length; index++) {
            //sprites[index].camera = camera;
            //render_event.target = sprites[index];
            render_event.camera = camera;
            sprites[index].dispatchEvent(render_event);
        }
    };

    ///////////////////////////////
    //////////// Edisodes
    ///////////////////////////////

    setEpisode(category, episode) {
        that.episode.setEpisode(category, episode, that.on_episode_selected);
    };

    on_episode_selected(library) {
        for(var i in user_interfaces) {
            var frame = document.getElementById(user_interfaces[i].id+"-frame");
            if(frame && frame.contentWindow.on_episode_selected)
                frame.contentWindow.on_episode_selected(library);
        }
        // Hide "Please select an episode" overlay
        that.hidePageOverlay();
        that.showPageOverlay("Loading Knowledge Base");
        if(that.ros) that.ros.close(); // force reconnect

        $.ajax({
            url: '/knowrob/reset',
            type: "POST",
            contentType: "application/json",
            dataType: "json"
        });
    };

    ///////////////////////////////
    //////////// Frames
    ///////////////////////////////

    showFrame(iface_name) {
        var frame_name = getInterfaceFrameName(iface_name);
        // Hide inactive frames
        for(var i in user_interfaces) {
            if(user_interfaces[i].id == frame_name) continue;
            $("#"+user_interfaces[i].id+"-frame").hide();
            $("#"+user_interfaces[i].id+"-frame").removeClass("selected-frame");
            $("#"+user_interfaces[i].id+"-menu").removeClass("selected-menu");
        }

        var new_src = getInterfaceSrc(iface_name);
        var frame = document.getElementById(frame_name+"-frame");
        var old_src = frame.src;
        if(!old_src.endsWith(new_src)) {
            frame.src = new_src;
            if(frame.contentWindow && frame.contentWindow.on_register_nodes)
                frame.contentWindow.on_register_nodes();
        }

        // Show selected frame
        $("#"+frame_name+"-frame").show();
        $("#"+frame_name+"-frame").addClass("selected-frame");
        $("#"+frame_name+"-menu").addClass("selected-menu");
        // Load menu items of active frame
        that.menu.updateFrameMenu(document.getElementById(frame_name+"-frame").contentWindow);
    };

    getActiveFrame() {
        var frame = document.getElementById(getActiveFrameName()+"-frame");
        if(frame) return frame.contentWindow;
        else return window;
        //else return undefined;
    };

    getInterfaceFrameName(iface) {
        for(var i in user_interfaces) {
            var elem = user_interfaces[i];
            if(elem.id == iface) return elem.id;
            for(var j in elem.interfaces) {
                if(elem.interfaces[j].id == iface) return elem.id;
            }
        }
    };

    getInterfaceSrc(iface) {
        for(var i in user_interfaces) {
            var elem = user_interfaces[i];
            if(elem.id == iface) return elem.src;
            for(var j in elem.interfaces) {
                if(elem.interfaces[j].id == iface) return elem.interfaces[j].src;
            }
        }
    };

    getActiveFrameName() {
        return getInterfaceFrameName(getActiveInterfaceName());
    };

    getActiveInterfaceName() {
        for(var i in user_interfaces_flat) {
            if(urlQuery[user_interfaces_flat[i].id]) return user_interfaces_flat[i].id;
        }
        return "kb";
    };

    ///////////////////////////////
    //////////// URL Location
    ///////////////////////////////

    updateQueryString() {
        urlQuery = {};
        var query = String(window.location.hash.substring(1));
        var vars = query.split("?");
        for (var i=0;i<vars.length;i++) {
            var pair = vars[i].split("=");
            if (typeof urlQuery[pair[0]] === "undefined") {
                // If first entry with this name
                urlQuery[pair[0]] = decodeURIComponent(pair[1]);
            }
            else if (typeof urlQuery[pair[0]] === "string") {
                // If second entry with this name
                var arr = [ urlQuery[pair[0]],decodeURIComponent(pair[1]) ];
                urlQuery[pair[0]] = arr;
            }
            else {
                // If third or later entry with this name
                urlQuery[pair[0]].push(decodeURIComponent(pair[1]));
            }
        }
    };

    updateLocation() {
        updateQueryString();
        showFrame(getActiveInterfaceName());
        // update episode selection from URL query
        // e.g., https://data.openease.org/#kb?category=foo?episode=bar
        if(urlQuery['category'] && urlQuery['episode']) {
            that.setEpisode(urlQuery['category'], urlQuery['episode']);
        }
    };

    ///////////////////////////////
    //////////// Frame Overlay
    ///////////////////////////////

    createIOSPageOverlay() {
        var page = document.getElementById('page');

        if(page) {
            var pageOverlay = this.createOverlayDiv();
            page.appendChild(pageOverlay);
            var spinner = createSpinner();
            pageOverlay.appendChild(spinner.el);
        }
    };

    createOverlayDiv() {
        var pageOverlay = document.createElement("div");

        pageOverlay.setAttribute("id", "page-overlay");
        pageOverlay.className = "ios-overlay ios-overlay-hide div-overlay";
        pageOverlay.innerHTML += '<span class="title">Please select an Episode</span>';
        pageOverlay.style.display = 'none';

        return pageOverlay;
    }

    showPageOverlay(text) {
        const pageOverlay = this.getPageOverlayDivFromDoc();
        if(this.isOverlayDisabled(pageOverlay)) {
            this.activateOverlay();
            this.setThatPageOverlayEnabled(true);
        }
    }

    getPageOverlayDivFromDoc() {
        return document.getElementById('page-overlay');
    }

    isOverlayDisabled(pageOverlay) {
        return pageOverlay && !this.getThatPageOverlayEnabled();
    }

    getThatPageOverlayEnabled() {
        return this.that.pageOverlayEnabled;
    }

    setThatPageOverlayEnabled(setEnabled) {
        this.that.pageOverlayEnabled = setEnabled;
    };

    activateOverlay() {
        pageOverlay.children[0].innerHTML = text;
        pageOverlay.style.display = 'block';
        pageOverlay.className = pageOverlay.className.replace("hide","show");
        pageOverlay.style.pointerEvents = "auto";
    }

    hidePageOverlay () {
        const pageOverlay = this.getPageOverlayDivFromDoc();
        if(this.isOverlayEnabled(pageOverlay)) {
            this.deactivateOverlay();
            this.setThatPageOverlayEnabled(false);
        }
    };

    isOverlayEnabled(pageOverlay) {
        return pageOverlay && this.getThatPageOverlayEnabled();
    }

    deactivateOverlay() {
        //pageOverlay.style.display = 'none';
        pageOverlay.className = pageOverlay.className.replace("show","hide");
        pageOverlay.style.pointerEvents = "none";
    }
}

module.exports = {
    KnowrobClient,
};
