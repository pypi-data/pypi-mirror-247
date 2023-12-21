function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function onRender(event) {
  if (!window.rendered) {
    const {video, mimetype, track} = event.detail.args

    sendValue({video: video, mimetype: mimetype, track: track})
    window.rendered = true
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(399)
