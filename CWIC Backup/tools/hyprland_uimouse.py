#!/usr/bin/env python3
"""Minimal absolute-ish mouse over /dev/uinput, driven by hyprctl cursorpos feedback."""
import fcntl, struct, subprocess, sys, time

UI_SET_EVBIT, UI_SET_KEYBIT, UI_SET_RELBIT = 0x40045564, 0x40045565, 0x40045566
UI_DEV_CREATE, UI_DEV_DESTROY = 0x5501, 0x5502
EV_SYN, EV_KEY, EV_REL = 0x00, 0x01, 0x02
REL_X, REL_Y, REL_WHEEL = 0x00, 0x01, 0x08
BTN_LEFT, BTN_RIGHT = 0x110, 0x111


class Mouse:
    def __init__(self):
        self.fd = open("/dev/uinput", "wb", buffering=0)
        for bit in (EV_KEY, EV_REL, EV_SYN):
            fcntl.ioctl(self.fd, UI_SET_EVBIT, bit)
        for bit in (BTN_LEFT, BTN_RIGHT):
            fcntl.ioctl(self.fd, UI_SET_KEYBIT, bit)
        for bit in (REL_X, REL_Y, REL_WHEEL):
            fcntl.ioctl(self.fd, UI_SET_RELBIT, bit)
        # struct uinput_user_dev: name[80], id{bus,vendor,product,version},
        # ff_effects_max, absmax/absmin/absfuzz/absflat [64] each
        dev = b"claude-uimouse".ljust(80, b"\0") + struct.pack("HHHH", 0x03, 0x1234, 0x5678, 1)
        dev += struct.pack("i", 0) + b"\0" * (4 * 64 * 4)
        self.fd.write(dev)
        fcntl.ioctl(self.fd, UI_DEV_CREATE)
        time.sleep(0.6)

    def _emit(self, etype, code, value):
        self.fd.write(struct.pack("llHHi", 0, 0, etype, code, value))

    def _syn(self):
        self._emit(EV_SYN, 0, 0)

    def move_rel(self, dx, dy):
        step = 40
        while dx or dy:
            sx = max(-step, min(step, dx))
            sy = max(-step, min(step, dy))
            if sx:
                self._emit(EV_REL, REL_X, sx)
            if sy:
                self._emit(EV_REL, REL_Y, sy)
            self._syn()
            dx -= sx
            dy -= sy
            time.sleep(0.002)

    @staticmethod
    def pos():
        out = subprocess.run(["hyprctl", "cursorpos"], capture_output=True, text=True).stdout
        x, y = out.strip().split(",")
        return int(x), int(y)

    # The compositor swallows small relative deltas and scales the rest to
    # roughly 0.30x, so requested moves are pre-multiplied and floored.
    GAIN = 3.4
    MIN_STEP = 4

    def _scale(self, err):
        if err == 0:
            return 0
        v = int(round(err * self.GAIN))
        if abs(v) < self.MIN_STEP:
            v = self.MIN_STEP if err > 0 else -self.MIN_STEP
        return v

    def goto(self, x, y, tries=40):
        self.move_rel(-9000, -9000)  # pin to desktop origin
        time.sleep(0.15)
        for _ in range(tries):
            cx, cy = self.pos()
            if (cx, cy) == (x, y):
                return True
            self.move_rel(self._scale(x - cx), self._scale(y - cy))
            time.sleep(0.03)
        return self.pos() == (x, y)

    def click(self, x=None, y=None, button=BTN_LEFT, double=False):
        if x is not None:
            self.goto(x, y)
            time.sleep(0.15)
        for _ in range(2 if double else 1):
            self._emit(EV_KEY, button, 1)
            self._syn()
            time.sleep(0.05)
            self._emit(EV_KEY, button, 0)
            self._syn()
            time.sleep(0.08)
        time.sleep(0.35)

    def close(self):
        fcntl.ioctl(self.fd, UI_DEV_DESTROY)
        self.fd.close()


if __name__ == "__main__":
    m = Mouse()
    try:
        cmd = sys.argv[1]
        if cmd == "pos":
            print(m.pos())
        elif cmd == "goto":
            ok = m.goto(int(sys.argv[2]), int(sys.argv[3]))
            print("at", m.pos(), "exact" if ok else "APPROX")
        elif cmd == "click":
            m.click(int(sys.argv[2]), int(sys.argv[3]))
            print("clicked", m.pos())
        elif cmd == "dclick":
            m.click(int(sys.argv[2]), int(sys.argv[3]), double=True)
            print("double-clicked", m.pos())
    finally:
        m.close()
