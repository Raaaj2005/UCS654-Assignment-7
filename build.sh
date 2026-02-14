#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

echo "Installing FFmpeg..."
mkdir -p ffmpeg_bin
curl -L https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz | tar xJ -C ffmpeg_bin --strip-components 1

export PATH=$PATH:$(pwd)/ffmpeg_bin
