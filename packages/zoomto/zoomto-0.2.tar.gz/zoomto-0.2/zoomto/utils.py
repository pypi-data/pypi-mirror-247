from zrcl3.win_process import get_pid_from_hwnd
from zrcl3.orjson_io_fallback import load_json, save_json
from zrcl3.desktop_automation import capture_window, find_word_coordinates
from zrcl3.singleton import SingletonMeta
from zrcl3.expirable_property import TimelyCachedProperty
from zrcl3.auto_save_dict.on_trigger import OnChangeSaveDict
