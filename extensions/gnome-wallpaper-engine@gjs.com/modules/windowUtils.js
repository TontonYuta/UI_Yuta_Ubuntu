export class WindowUtils {
    static isWallpaperWindow(metaWin) {
        if (!metaWin) return false;

        const title = metaWin.get_title ? metaWin.get_title() : "";
        const wmClass = metaWin.get_wm_class ? metaWin.get_wm_class() : "";
        const gtkAppId = metaWin.get_gtk_application_id ? metaWin.get_gtk_application_id() : "";
        const sandboxedId = metaWin.get_sandboxed_app_id ? metaWin.get_sandboxed_app_id() : "";

        return (
            title === "wallpaper_bg" ||
            wmClass === "wallpaper_bg" ||
            gtkAppId === "wallpaper_bg" ||
            sandboxedId === "wallpaper_bg"
        );
    }

    static _isWindowMaximized(metaWin) {
        if (typeof metaWin.is_maximized === "function") {
            return metaWin.is_maximized();
        } else {
            return metaWin.get_maximized ? metaWin.get_maximized() === 3 : false;
        }
    }

    static isFullscreenLike(metaWin) {
        if (!metaWin) return false;
        return metaWin.is_fullscreen() || this._isWindowMaximized(metaWin);
    }

    static fillsMonitor(metaWin) {
        if (!metaWin) return false;
        if (metaWin.is_fullscreen()) return true;
        if (this._isWindowMaximized(metaWin)) return true;

        const monitorIndex = metaWin.get_monitor();
        if (monitorIndex < 0) return false;

        const monitor = global.display.get_monitor_geometry(monitorIndex);
        const rect = metaWin.get_frame_rect();

        const tolerance = 10;

        return (
            Math.abs(rect.x - monitor.x) < tolerance &&
            Math.abs(rect.y - monitor.y) < tolerance &&
            Math.abs(rect.width - monitor.width) < tolerance &&
            Math.abs(rect.height - monitor.height) < tolerance
        );
    }
}
