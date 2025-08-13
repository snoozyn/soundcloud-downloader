#!/bin/bash

# SoundCloud Downloader (Bash + yt-dlp + ffmpeg)
# Downloads as 256kbps AAC (with Premium OAuth token) and converts to 320kbps MP3 with full metadata
# Requires yt-dlp and ffmpeg installed
# Reads OAuth token from .env file or prompts user if not found

# Check if dependencies are installed
if ! command -v yt-dlp &> /dev/null || ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: yt-dlp and ffmpeg are required. Please install them."
    exit 1
fi

DOWNLOADS_DIR="$HOME/Music/SoundCloud"
mkdir -p "$DOWNLOADS_DIR"
TEMP_DIR="$DOWNLOADS_DIR/temp"
mkdir -p "$TEMP_DIR"

EXIT_COMMANDS=("exit" "q")

# Load OAuth token from .env file if it exists
if [[ -f .env ]]; then
    source .env
fi

# Check if OAuth token is set in .env, otherwise prompt user
if [[ -z "$SOUNDCLOUD_OAUTH_TOKEN" ]]; then
    echo "To download high-quality AAC (256kbps), provide your SoundCloud Premium OAuth token."
    echo "Guide to find token: https://blog.rtrace.io/posts/youtube-dl/#Authentication-against-Soundcloud"
    echo -n "Enter OAuth token (or press Enter to skip for standard quality): "
    read OAUTH_TOKEN
else
    OAUTH_TOKEN="$SOUNDCLOUD_OAUTH_TOKEN"
fi

# Validate OAuth token (only check if non-empty)
if [[ -z "$OAUTH_TOKEN" ]]; then
    echo "⚠️ Warning: No OAuth token provided. Continuing without it for standard quality."
    OAUTH_TOKEN=""
fi

while true; do
    echo -n "Enter SoundCloud URL (or 'q' to quit): "
    read URL

    # Exit check
    for cmd in "${EXIT_COMMANDS[@]}"; do
        if [[ "$URL" == "$cmd" ]]; then
            echo "Goodbye!"
            rm -rf "$TEMP_DIR"
            exit 0
        fi
    done

    # URL validation
    if [[ ! "$URL" =~ ^https?://(www\.)?soundcloud\.com/.*$ ]]; then
        echo "❌ Invalid SoundCloud URL."
        continue
    fi

    echo "🎧 Downloading as 256kbps AAC (if available) and converting to 320kbps MP3 with metadata..."
    # Download as AAC with OAuth token (if provided) and extract metadata
    if [[ -n "$OAUTH_TOKEN" ]]; then
        yt-dlp \
            --add-header "Authorization: OAuth $OAUTH_TOKEN" \
            -f "bestaudio" \
            --extract-audio \
            --audio-format aac \
            --audio-quality 256k \
            --embed-thumbnail \
            --add-metadata \
            --parse-metadata "title:%(track)s" \
            --parse-metadata "uploader:%(artist)s" \
            --parse-metadata "genre:%(genre)s" \
            --output "$TEMP_DIR/%(title)s - %(uploader)s.%(ext)s" \
            "$URL"
    else
        yt-dlp \
            -f "bestaudio" \
            --extract-audio \
            --audio-format aac \
            --audio-quality 256k \
            --embed-thumbnail \
            --add-metadata \
            --parse-metadata "title:%(track)s" \
            --parse-metadata "uploader:%(artist)s" \
            --parse-metadata "genre:%(genre)s" \
            --output "$TEMP_DIR/%(title)s - %(uploader)s.%(ext)s" \
            "$URL"
    fi

    if [[ $? -ne 0 ]]; then
        echo "❌ Download failed. Note: Some tracks may only be available in 128kbps MP3."
        continue
    fi

    # Find the downloaded AAC or M4A file
    AUDIO_FILE=$(find "$TEMP_DIR" -type f \( -name "*.aac" -o -name "*.m4a" \) -print -quit)
    if [[ -z "$AUDIO_FILE" ]]; then
        echo "❌ No AAC or M4A file found."
        continue
    fi

    # Convert AAC/M4A to 320kbps MP3
    OUTPUT_FILE="${AUDIO_FILE%.*}.mp3"
    ffmpeg -i "$AUDIO_FILE" \
           -c:a mp3 \
           -b:a 320k \
           -map_metadata 0 \
           -id3v2_version 3 \
           "$DOWNLOADS_DIR/$(basename "${OUTPUT_FILE}")"

    if [[ $? -eq 0 ]]; then
        echo "✅ Conversion complete! Saved to $DOWNLOADS_DIR"
        # Clean up temporary AAC/M4A file
        rm "$AUDIO_FILE"
    else
        echo "❌ Conversion failed."
    fi
done

# Clean up temp directory on script exit
rm -rf "$TEMP_DIR"
