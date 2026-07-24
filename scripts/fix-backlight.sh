#!/bin/sh

BACKLIGHT_DIR="/sys/class/backlight/intel_backlight"
SAVED_STATE="/tmp/saved_brightness"

case $1/$2 in
  pre/*)
    if [ -f "$BACKLIGHT_DIR/brightness" ]; then
      cp "$BACKLIGHT_DIR/brightness" "$SAVED_STATE"
    fi
    ;;
  post/*)
    if [ -f "$SAVED_STATE" ]; then
      sleep 0.5
      cp "$SAVED_STATE" "$BACKLIGHT_DIR/brightness"
    fi
    ;;
esac
