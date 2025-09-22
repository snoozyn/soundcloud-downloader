#!/bin/bash

# SoundCloud Downloader (Bash + yt-dlp + ffmpeg)
<<<<<<< HEAD
# Downloads as 320kbps MP3 with full metadata
# Requires yt-dlp and ffmpeg to be installed
=======
# Downloads as 256kbps AAC (with Premium OAuth token) and converts to 320kbps MP3 with full metadata
# Requires yt-dlp and ffmpeg installed
# Reads OAuth token from .env file or prompts user if not found
>>>>>>> 06563489fa39f070645fddc211cdeb7948d653a6

# Check if dependencies are installed
if ! command -v yt-dlp &> /dev/null || ! command -v ffmpeg &> /dev/null; then
    echo "❌ Error: yt-dlp and ffmpeg are required. Please install them."
    exit 1
fi

<<<<<<< HEAD
DOWNLOADS_DIR="$HOME/Downloads"
mkdir -p "$DOWNLOADS_DIR"

EXIT_COMMANDS=("exit" "q")

=======
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

>>>>>>> 06563489fa39f070645fddc211cdeb7948d653a6
while true; do
    echo -n "Enter SoundCloud URL (or 'q' to quit): "
    read URL

    # Exit check
    for cmd in "${EXIT_COMMANDS[@]}"; do
        if [[ "$URL" == "$cmd" ]]; then
            echo "Goodbye!"
<<<<<<< HEAD
=======
            rm -rf "$TEMP_DIR"
>>>>>>> 06563489fa39f070645fddc211cdeb7948d653a6
            exit 0
        fi
    done

    # URL validation
    if [[ ! "$URL" =~ ^https?://(www\.)?soundcloud\.com/.*$ ]]; then
        echo "❌ Invalid SoundCloud URL."
        continue
    fi

<<<<<<< HEAD
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
=======
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
>>>>>>> 06563489fa39f070645fddc211cdeb7948d653a6

    if [[ $? -ne 0 ]]; then
        echo "❌ Download failed. Note: Some tracks may only be available in 128kbps MP3."
        continue
    fi

<<<<<<< HEAD
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
=======
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
>>>>>>> 06563489fa39f070645fddc211cdeb7948d653a6
