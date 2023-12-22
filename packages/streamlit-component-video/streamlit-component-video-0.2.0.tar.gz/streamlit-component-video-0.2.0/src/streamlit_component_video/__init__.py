import io
import uuid
from pathlib import Path
from typing import Union

import streamlit as st
from streamlit import runtime
from streamlit.runtime import caching
from streamlit.components.v1 import declare_component

frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = declare_component(
    "streamlit_component_video", path=str(frontend_dir)
)


def get_media_url(data: str, mimetype: str) -> str:
    data_or_filename: Union[bytes, str]
    if not data:
        return ""
    if isinstance(data, (str, bytes)):
        data_or_filename = data
    elif isinstance(data, io.BytesIO):
        data.seek(0)
        data_or_filename = data.getvalue()
    elif isinstance(data, io.RawIOBase) or isinstance(data, io.BufferedReader):
        data.seek(0)
        read_data = data.read()
        if read_data is None:
            return ""
        else:
            data_or_filename = read_data
    else:
        raise RuntimeError("Invalid binary data format: %s" % type(data))

    coordinates = str(uuid.uuid4())

    if runtime.exists():
        file_url = runtime.get_instance().media_file_mgr.add(
            data_or_filename, mimetype, coordinates
        )
        caching.save_media_data(data_or_filename, mimetype, coordinates)
    else:
        file_url = ""
    return file_url


def streamlit_component_video(
    video: str | Path,
    mimetype: str,  # e.g. video/mp4
    track: str = None,
    key: str = None,
):
    """Create a new instance of "streamlit_component_video"."""
    component_value = _component_func(
        video=get_media_url(video, mimetype),
        mimetype=mimetype,
        track=get_media_url(track, "text/vtt"),
        key=key,
    )

    return component_value