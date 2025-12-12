#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
CHECKMARK="✅"
ERROR="❌"
SPINNER="⏳"

# Check if terminal supports colors
tput colors >/dev/null 2>&1 && SUPPORTS_COLORS=1 || SUPPORTS_COLORS=0

# Function to print colored messages
print_message() {
    local color=$1
    local emoji=$2
    local message=$3
    if [ $SUPPORTS_COLORS -eq 1 ]; then
        echo -e "${color}${emoji} ${message}${NC}"
    else
        echo -e "${emoji} ${message}"
    fi
}

# Fallback spinner function
spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\\'
    while kill -0 $pid 2>/dev/null; do
        local temp=${spinstr#?}
        printf "\r%s Processing... %s" "$SPINNER" "${spinstr:0:1}"
        spinstr=$temp${spinstr%"$temp"}
        sleep $delay
    done
    printf "\r%*s\r" "$(tput cols)" "" # Clear the line
}

# Function to get the user's downloads directory
get_downloads_dir() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        echo "$HOME/Downloads"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        echo "$HOME/Downloads"
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
        echo "$USERPROFILE/Downloads"
    else
        echo "$HOME/Downloads" # Fallback
    fi
}

# Function to validate SoundCloud URL
validate_url() {
    local url=$1
    if [[ $url =~ ^https?://(www\.)?soundcloud\.com/.+ ]]; then
        return 0
    else
        return 1
    fi
}

# Function to convert string to lowercase (compatible with older Bash)
to_lowercase() {
    local input=$1
    echo "$input" | tr '[:upper:]' '[:lower:]'
}

# Function to extract metadata from yt-dlp JSON output
extract_metadata() {
    local json_file=$1
    local title=$(jq -r '.title // empty' "$json_file" 2>/dev/null || echo "")
    local uploader=$(jq -r '.uploader // empty' "$json_file" 2>/dev/null || echo "")
    local duration=$(jq -r '.duration // empty' "$json_file" 2>/dev/null || echo "")
    local upload_date=$(jq -r '.upload_date // empty' "$json_file" 2>/dev/null || echo "")

    # Format upload date if available
    local formatted_date=""
    if [[ -n "$upload_date" && ${#upload_date} -eq 8 ]]; then
        formatted_date=$(date -d "${upload_date:0:4}-${upload_date:4:2}-${upload_date:6:2}" +"%B %d, %Y" 2>/dev/null || echo "$upload_date")
    fi

    echo "title='$title'"
    echo "artist='$uploader'"
    echo "duration='$duration'"
    echo "upload_date='$formatted_date'"
}

# Function to detect Camelot key using keyfinder-cli
detect_camelot_key() {
    local audio_file=$1
    local camelot_key=""

    if command -v keyfinder-cli &> /dev/null; then
        camelot_key=$(keyfinder-cli -n camelot "$audio_file" 2>/dev/null)
        if [[ -z "$camelot_key" ]]; then
            camelot_key="Not detected"
        fi
    else
        camelot_key="keyfinder-cli not installed"
    fi

    echo "$camelot_key"
}

# Function to detect max frequency using sox
detect_max_khz() {
    local audio_file=$1
    local max_khz=""

    if command -v sox &> /dev/null; then
        # Get sample rate and calculate max frequency (Nyquist frequency = sample rate / 2)
        local sample_rate=$(soxi -r "$audio_file" 2>/dev/null)
        if [[ -n "$sample_rate" && "$sample_rate" =~ ^[0-9.]+$ ]]; then
            local nyquist_freq=$(awk "BEGIN {printf \"%.0f\", $sample_rate / 2000}")
            max_khz="${nyquist_freq} kHz"
        else
            max_khz="Not detected"
        fi
    else
        max_khz="sox not installed"
    fi

    echo "$max_khz"
}

# Function to display file analysis
analyze_file() {
    local audio_file=$1
    local json_file="$2"

    print_message "$YELLOW" "ℹ" "Analyzing audio file..."

    # Extract metadata
    eval $(extract_metadata "$json_file")

    # Display basic metadata
    print_message "$GREEN" "🎵" "Title: $title"
    print_message "$GREEN" "👤" "Artist: $artist"

    if [[ -n "$duration" ]]; then
        local duration_min=$(awk "BEGIN {printf \"%.1f\", $duration / 60}")
        print_message "$GREEN" "⏱️" "Duration: ${duration_min}min"
    fi

    if [[ -n "$upload_date" ]]; then
        print_message "$GREEN" "📅" "Upload Date: $upload_date"
    fi

    echo

    # Analyze technical details
    print_message "$YELLOW" "🔍" "Technical Analysis:"

    # Camelot key
    local camelot_key=$(detect_camelot_key "$audio_file")
    print_message "$GREEN" "🎹" "Camelot Key: $camelot_key"

    # Max frequency
    local max_khz=$(detect_max_khz "$audio_file")
    print_message "$GREEN" "📊" "Max Frequency: $max_khz"

    echo
}

# Function to download song or playlist
download_song() {
    local url=$1
    local download_type=$2
    local downloads_folder=$(get_downloads_dir)
    local temp_output=$(mktemp)
    local temp_json=$(mktemp)

    # Set output template based on download type
    if [ "$download_type" == "single" ]; then
        output_template="$downloads_folder/%(title)s - %(uploader)s.%(ext)s"
        json_template="$downloads_folder/%(title)s - %(uploader)s.json"
    else
        output_template="$downloads_folder/%(playlist_title)s/%(title)s - %(uploader)s.%(ext)s"
        json_template="$downloads_folder/%(playlist_title)s/%(title)s - %(uploader)s.json"
    fi

    # Build yt-dlp command with JSON output for metadata
    local command=("yt-dlp" "--extract-audio" "--audio-format" "mp3" "--audio-quality" "320K" "--output" "$output_template" "--embed-metadata" "--embed-thumbnail" "--write-info-json" "--progress" "--newline")
    if [ "$download_type" == "playlist" ]; then
        command+=("--yes-playlist")
    fi
    command+=("$url")

    # Run download in background and capture output
    print_message "$YELLOW" "ℹ" "Starting download..."
    "${command[@]}" >"$temp_output" 2>&1 &
    local pid=$!
    spinner "$pid"

    # Wait for the command to finish and check exit status
    wait $pid
    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        print_message "$GREEN" "$CHECKMARK" "Download complete! Files saved to $downloads_folder"

        # Find the downloaded file and JSON
        local audio_file=""
        local json_file=""

        if [ "$download_type" == "single" ]; then
            # For single downloads, look for the most recently created MP3
            audio_file=$(find "$downloads_folder" -name "*.mp3" -type f -mtime -1 -print0 | xargs -0 ls -t | head -1)
            json_file=$(find "$downloads_folder" -name "*.json" -type f -mtime -1 -print0 | xargs -0 ls -t | head -1)
        else
            # For playlists, look in the playlist directory
            local playlist_dir=$(find "$downloads_folder" -maxdepth 1 -type d -name "*$(basename "$url")*" -o -name "*playlist*" 2>/dev/null | head -1)
            if [[ -n "$playlist_dir" ]]; then
                audio_file=$(find "$playlist_dir" -name "*.mp3" -type f -mtime -1 -print0 | xargs -0 ls -t | head -1)
                json_file=$(find "$playlist_dir" -name "*.json" -type f -mtime -1 -print0 | xargs -0 ls -t | head -1)
            fi
        fi

        # If we found files, analyze them
        if [[ -n "$audio_file" && -f "$audio_file" && -n "$json_file" && -f "$json_file" ]]; then
            analyze_file "$audio_file" "$json_file"
        else
            print_message "$YELLOW" "ℹ" "Could not locate downloaded file for analysis."
        fi

        rm -f "$temp_output" "$temp_json"
        return 0
    else
        print_message "$RED" "$ERROR" "Download failed. Please check the URL and try again." >&2
        print_message "$YELLOW" "ℹ" "Check /tmp/yt-dlp-debug.log for details." >&2
        cat "$temp_output" >> /tmp/yt-dlp-debug.log 2>/dev/null || true
        rm -f "$temp_output" "$temp_json"
        return $exit_code
    fi
}

# Main CLI function
main() {
    # Welcome message with example
    print_message "$GREEN" "$CHECKMARK" "Welcome to the SoundCloud Downloader CLI!"
    echo "Example usage:"
    echo "  Enter a SoundCloud URL like https://soundcloud.com/artist/song"
    echo "  Choose '1' for a single track or '2' for a playlist"
    echo
    print_message "$YELLOW" "ℹ" "Note: For full analysis, install sox and keyfinder-cli (uses libkeyfinder):"
    echo "  Linux: sudo apt install sox cmake libkeyfinder-dev libfftw3-dev (then build keyfinder-cli from source)"
    echo "  macOS: brew install sox cmake libkeyfinder fftw"
    echo "         git clone https://github.com/EvanPurkhiser/keyfinder-cli.git"
    echo "         cd keyfinder-cli"
    echo "         cmake -DCMAKE_INSTALL_PREFIX=/usr/local -S . -B build"
    echo "         cmake --build build"
    echo "         cmake --install build"
    echo

    while true; do
        # Prompt for URL
        read -p "Enter the SoundCloud URL (or 'q' to quit): " url
        url_lower=$(to_lowercase "$url")
        if [[ "$url_lower" == "q" || "$url_lower" == "exit" ]]; then
            print_message "$GREEN" "$CHECKMARK" "Goodbye!"
            exit 0
        fi

        # Validate URL
        if ! validate_url "$url"; then
            print_message "$RED" "$ERROR" "Invalid SoundCloud URL. Please ensure it starts with https://soundcloud.com/." >&2
            print_message "$YELLOW" "ℹ" "Example: https://soundcloud.com/artist/song" >&2
            continue
        fi

        # Prompt for download type
        read -p "Select download type (1=Single, 2=Playlist): " choice
        choice_lower=$(to_lowercase "$choice")
        case "$choice_lower" in
            1 | single)
                download_song "$url" "single"
                if [ $? -ne 0 ]; then
                    continue
                fi
                ;;
            2 | playlist)
                download_song "$url" "playlist"
                if [ $? -ne 0 ]; then
                    continue
                fi
                ;;
            *)
                print_message "$RED" "$ERROR" "Invalid choice. Please enter '1' for Single or '2' for Playlist." >&2
                continue
                ;;
        esac
    done
}

# Check if yt-dlp is installed
if ! command -v yt-dlp >/dev/null 2>&1; then
    print_message "$RED" "$ERROR" "yt-dlp is not installed. Please install it first." >&2
    print_message "$YELLOW" "ℹ" "You can install yt-dlp using: sudo apt install yt-dlp (Linux) or brew install yt-dlp (macOS)" >&2
    exit 1
fi

# Check if jq is installed (for JSON parsing)
if ! command -v jq >/dev/null 2>&1; then
    print_message "$YELLOW" "⚠" "jq is not installed. Metadata extraction will be limited." >&2
    print_message "$YELLOW" "ℹ" "Install with: sudo apt install jq (Linux) or brew install jq (macOS)" >&2
fi

# Check for keyfinder-cli
if ! command -v keyfinder-cli >/dev/null 2>&1; then
    print_message "$YELLOW" "ℹ" "keyfinder-cli not found. Camelot key detection will not work. See installation notes above."
else
    print_message "$GREEN" "$CHECKMARK" "keyfinder-cli found."
fi

# Check Bash version for compatibility
if [ "${BASH_VERSINFO[0]}" -lt 4 ]; then
    print_message "$YELLOW" "ℹ" "You are using Bash ${BASH_VERSINFO[0]}.${BASH_VERSINFO[1]}. Some features may require Bash 4.0 or higher for full compatibility." >&2
fi

# Run the main function
main
