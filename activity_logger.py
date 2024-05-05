#!/usr/bin/env python3
 
import Xlib # type: ignore
import Xlib.display # type: ignore
import datetime;

disp = Xlib.display.Display()
root = disp.screen().root

NET_ACTIVE_WINDOW = disp.intern_atom('_NET_ACTIVE_WINDOW')
NET_WM_NAME = disp.intern_atom('_NET_WM_NAME')

last_seen = {'xid': None}
def get_active_window():
    window_id = root.get_full_property(NET_ACTIVE_WINDOW,Xlib.X.AnyPropertyType).value[0]

    focus_changed = (window_id != last_seen['xid'])
    last_seen['xid'] = window_id

    return window_id, focus_changed

def get_window_name(window_id):
    try:
        window_obj = disp.create_resource_object('window', window_id)
        window_name = window_obj.get_full_property(NET_WM_NAME, 0).value
    except Xlib.error.XError:
        window_name = None

    return window_name


if __name__ == '__main__':
    ct_last = datetime.datetime.now()
    root.change_attributes(event_mask=Xlib.X.PropertyChangeMask)
    filename = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".csv"
    while True:
        win, changed = get_active_window()
        if changed:
            ct = datetime.datetime.now()
            time_diff = (ct - ct_last).total_seconds() / 60  # Calculate time difference in minutes
            print(ct, ", ", ct - ct_last, ", ", time_diff, ", ", "\"", get_window_name(win), "\"")

            with open(filename, "a") as file1:
                file1.write(f"{ct}, {ct - ct_last}, {time_diff}, \"{get_window_name(win)}\"\n")

            ct_last = ct

        while True:
            event = disp.next_event()
            if (event.type == Xlib.X.PropertyNotify and
                    event.atom == NET_ACTIVE_WINDOW):
                break
