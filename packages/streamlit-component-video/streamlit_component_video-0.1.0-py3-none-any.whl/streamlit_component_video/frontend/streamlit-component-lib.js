function sendMessageToStreamlitClient(type, data) {
  const outData = Object.assign({
      isStreamlitMessage: true,
      type: type,
  }, data);
  window.parent.postMessage(outData, "*");
}

const Streamlit = {
  setComponentReady: function() {
      sendMessageToStreamlitClient("streamlit:componentReady", {apiVersion: 1});
  },
  setFrameHeight: function(height) {
      sendMessageToStreamlitClient("streamlit:setFrameHeight", {height: height});
  },
  setComponentValue: function(value) {
    sendMessageToStreamlitClient("streamlit:setComponentValue", {value: value});
    var options = {
      tracks: [{
        id: 'alternate-video-track',
        src: value['track'],
        kind:'subtitles',
        srclang: 'en',
        label: 'English',
        mode: 'showing'
      }],
      sources: [{
        src: value['video'],
        type: value['mimetype']
      }]
    };
    var player = videojs('my-player', options, function onPlayerReady() {
      function myfun() {
        console.log("myPlayer.currentTime()", this.currentTime());
      }

      this.on("timeupdate", myfun);

      this.on('paused', function() {
        var track = options['tracks'][0];
        this.videoTracks().removeTrack(track);
        this.videoTracks().addTrack(track);
      });
    });
    player.controlBar.progressControl.disable();
  },
  RENDER_EVENT: "streamlit:render",
  events: {
    addEventListener: function(type, callback) {
      window.addEventListener("message", function(event) {
        if (event.data.type === type) {
          event.detail = event.data
          callback(event);
        }
      });
    }
  }
}
