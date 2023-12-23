function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function onRender(event) {
  if (!window.rendered) {
    const {path, mimetype, track, current_time} = event.detail.args

    if (path != "" && mimetype != "" && track != "") {
      sendValue({path: path, mimetype: mimetype, track: track, current_time: current_time})
      window.rendered = true
    }
  }
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
Streamlit.setFrameHeight(399)
