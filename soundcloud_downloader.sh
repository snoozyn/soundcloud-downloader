#!/bin/bash

# SoundCloud Downloader (Bash + yt-dlp + ffmpeg)
# Downloads as 320kbps MP3 with full metadata
# Requires yt-dlp and ffmpeg to be installed

# Check if dependencies are installed
if ! command -v yt-dlp &> /dev/null || ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: yt-dlp and ffmpeg are required. Please install them."
    exit 1
fi

DOWNLOADS_DIR="$HOME/Downloads"
mkdir -p "$DOWNLOADS_DIR"

EXIT_COMMANDS=("exit" "q")

while true; do
    echo -n "Enter SoundCloud URL (or 'q' to quit): "
    read URL

    # Exit check
    for cmd in "${EXIT_COMMANDS[@]}"; do
        if [[ "$URL" == "$cmd" ]]; then
            echo "Goodbye!"
            exit 0
        fi
    done

    # URL validation
    if [[ ! "$URL" =~ ^https?://(www\.)?soundcloud\.com/.*$ ]]; then
        echo "❌ Invalid SoundCloud URL."
        continue
    fi

    echo "🎧 Downloading as 320kbps MP3 with metadata..."

    # Define the output template
    OUTPUT_TEMPLATE="$DOWNLOADS_DIR/%(title)s - %(uploader)s.%(ext)s"

    # Download as MP3 and extract metadata
    yt-dlp \
        -f "bestaudio" \
        --extract-audio \
        --audio-format mp3 \
        --audio-quality 0 \
        --embed-thumbnail \
        --add-metadata \
        --parse-metadata "title:%(track)s" \
        --parse-metadata "uploader:%(artist)s" \
        --parse-metadata "genre:%(genre)s" \
        --parse-metadata "album:%(playlist)s" \
        --output "$OUTPUT_TEMPLATE" \
        "$URL"

    if [[ $? -ne 0 ]]; then
        echo "❌ Download failed. Note: Some tracks may only be available in 128kbps MP3."
        continue
    fi

    # Get the actual filename of the downloaded mp3
    DOWNLOADED_FILE=$(yt-dlp --get-filename -o "$OUTPUT_TEMPLATE" "$URL" --audio-format mp3)

    if [[ ! -f "$DOWNLOADED_FILE" ]]; then
        echo "❌ Downloaded file not found!"
        continue
    fi

    echo -n "Enter Key in Camelot (e.g., 8A or 11B) or press Enter to skip: "
    read CAMELOT_KEY

    if [[ -n "$CAMELOT_KEY" ]]; then
        # Get existing metadata
        TITLE=$(ffprobe -v error -show_entries format_tags=title -of default=noprint_wrappers=1:nokey=1 "$DOWNLOADED_FILE" 2>/dev/null || echo "")
        ARTIST=$(ffprobe -v error -show_entries format_tags=artist -of default=noprint_wrappers=1:nokey=1 "$DOWNLOADED_FILE" 2>/dev/null || echo "")
        GENRE=$(ffprobe -v error -show_entries format_tags=genre -of default=noprint_wrappers=1:nokey=1 "$DOWNLOADED_FILE" 2>/dev/null || echo "")
        ALBUM=$(ffprobe -v error -show_entries format_tags=album -of default=noprint_wrappers=1:nokey=1 "$DOWNLOADED_FILE" 2>/dev/null || echo "")

        # Create a temporary file for metadata update
        TEMP_FILE="$DOWNLOADED_FILE.tmp.mp3"
        ffmpeg -i "$DOWNLOADED_FILE" -c copy \
            -metadata title="$TITLE" \
            -metadata artist="$ARTIST" \
            -metadata genre="$GENRE" \
            -metadata album="$ALBUM" \
            -metadata comment="Key: $CAMELOT_KEY" \
            -y "$TEMP_FILE"

        if [[ $? -eq 0 ]]; then
            mv "$TEMP_FILE" "$DOWNLOADED_FILE"
            echo "✅ Metadata updated with Camelot Key."
        else
            echo "❌ Failed to update metadata."
            rm -f "$TEMP_FILE"
        fi
    fi

    echo "✅ Download complete! Saved to $DOWNLOADED_FILE"
done
