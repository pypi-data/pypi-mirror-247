def pygame_init_opengl(size=(0, 0), doublebuffer=True, vsync=True):
    import ctypes
    import pygame
    if hasattr(ctypes, "windll"):
        ctypes.windll.powrprof.PowerSetActiveScheme.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
        ctypes.windll.kernel32.SetPriorityClass.argtypes = [ctypes.c_void_p, ctypes.c_uint]
        ctypes.windll.kernel32.GetCurrentProcess.restype = ctypes.c_void_p
        ctypes.windll.powrprof.PowerSetActiveScheme(None, bytes.fromhex("da7f5e8cbfe8964a9a85a6e23a8c635c"))
        ctypes.windll.kernel32.SetPriorityClass(ctypes.windll.kernel32.GetCurrentProcess(), 0x80)
        ctypes.windll.shcore.SetProcessDpiAwareness(1)
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, 1)
    pygame.display.gl_set_attribute(pygame.GL_ACCELERATED_VISUAL, 1)
    pygame.display.gl_set_attribute(pygame.GL_DEPTH_SIZE, 0)
    pygame.display.gl_set_attribute(pygame.GL_STENCIL_SIZE, 0)
    flags = pygame.OPENGL
    if doublebuffer:
        flags |= pygame.DOUBLEBUF
    if size == (0, 0):
        flags |= pygame.FULLSCREEN
    pygame.display.set_mode(size, flags=flags, vsync=vsync)


def pygame_swap_buffers():
    import ctypes
    import pygame
    pygame.display.flip()
    if hasattr(ctypes, "windll"):
        ctypes.windll.dwmapi.DwmFlush()


def list_pixel_formats():
    import ctypes
    import struct
    if not hasattr(ctypes, "windll"):
        return []
    ctypes.windll.user32.GetActiveWindow.restype = ctypes.c_void_p
    ctypes.windll.user32.GetDC.argtypes = [ctypes.c_void_p]
    ctypes.windll.user32.GetDC.restype = ctypes.c_void_p
    ctypes.windll.gdi32.GetPixelFormat.argtypes = [ctypes.c_void_p]
    ctypes.windll.gdi32.DescribePixelFormat.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_void_p]
    hdc = ctypes.windll.user32.GetDC(ctypes.windll.user32.GetActiveWindow())
    pfd = struct.Struct("2HI20B3I")
    fields = [
        "nSize", "nVersion", "dwFlags", "iPixelType", "cColorBits", "cRedBits", "cRedShift", "cGreenBits",
        "cGreenShift", "cBlueBits", "cBlueShift", "cAlphaBits", "cAlphaShift", "cAccumBits", "cAccumRedBits",
        "cAccumGreenBits", "cAccumBlueBits", "cAccumAlphaBits", "cDepthBits", "cStencilBits", "cAuxBuffers",
        "iLayerType", "bReserved", "dwLayerMask", "dwVisibleMask", "dwDamageMask",
    ]
    buf = (ctypes.c_char * pfd.size)()
    hdc = ctypes.windll.user32.GetDC(ctypes.windll.user32.GetActiveWindow())
    num_formats = ctypes.windll.gdi32.DescribePixelFormat(hdc, 1, pfd.size, buf)
    pixel_formats = []
    for i in range(1, num_formats + 1):
        ctypes.windll.gdi32.DescribePixelFormat(hdc, i, pfd.size, buf)
        info = dict(zip(fields, pfd.unpack(bytes(buf))))
        info["iPixelFormat"] = i
        pixel_formats.append(info)
    return pixel_formats


def get_pixel_format():
    import ctypes
    if not hasattr(ctypes, "windll"):
        return 0
    ctypes.windll.user32.GetActiveWindow.restype = ctypes.c_void_p
    ctypes.windll.user32.GetDC.argtypes = [ctypes.c_void_p]
    ctypes.windll.user32.GetDC.restype = ctypes.c_void_p
    ctypes.windll.gdi32.GetPixelFormat.argtypes = [ctypes.c_void_p]
    hdc = ctypes.windll.user32.GetDC(ctypes.windll.user32.GetActiveWindow())
    pixel_format = ctypes.windll.gdi32.GetPixelFormat(hdc)
    return pixel_format


def get_refresh_rate():
    import ctypes
    import struct
    if not hasattr(ctypes, "windll"):
        return 60
    ctypes.windll.user32.GetActiveWindow.restype = ctypes.c_void_p
    ctypes.windll.user32.EnumDisplaySettingsA.argtypes = [ctypes.c_void_p, ctypes.c_int, ctypes.c_void_p]
    ctypes.windll.user32.MonitorFromWindow.argtypes = [ctypes.c_void_p, ctypes.c_int]
    ctypes.windll.user32.MonitorFromWindow.restype = ctypes.c_void_p
    ctypes.windll.user32.GetMonitorInfoA.argtypes = [ctypes.c_void_p, ctypes.c_void_p]
    buf = (ctypes.c_char * 72)()
    struct.pack_into("I", buf, 0, 72)
    monitor = ctypes.windll.user32.MonitorFromWindow(ctypes.windll.user32.GetActiveWindow(), 2)
    ctypes.windll.user32.GetMonitorInfoA(monitor, buf)
    display = buf.raw[40:buf.raw.index(b"\x00", 40)]
    buf = (ctypes.c_char * 156)()
    ctypes.windll.user32.EnumDisplaySettingsA(display, -1, buf)
    refresh_rate = struct.unpack("I", buf[120:124])[0]
    return refresh_rate


def get_dpi():
    import ctypes
    if not hasattr(ctypes, "windll"):
        return 72
    ctypes.windll.user32.GetActiveWindow.restype = ctypes.c_void_p
    dpi = ctypes.windll.user32.GetDpiForWindow(ctypes.windll.user32.GetActiveWindow())
    return dpi


def swap_interval(interval=1):
    import ctypes
    if not hasattr(ctypes, "windll"):
        return
    ctypes.windll.opengl32.wglGetProcAddress.argtypes = [ctypes.c_void_p]
    ctypes.windll.opengl32.wglGetProcAddress.restype = ctypes.c_void_p
    wglSwapIntervalEXT = ctypes.windll.opengl32.wglGetProcAddress(b"wglSwapIntervalEXT")
    ctypes.CFUNCTYPE(ctypes.c_int, ctypes.c_int)(wglSwapIntervalEXT)(interval)
