
import sys
import os

def convert_mp3_to_ogg(input_mp3_path):
    # Ensure input_mp3_path does not have 'MEDIA:' prefix
    if input_mp3_path.startswith("MEDIA:"):
        input_mp3_path = input_mp3_path[len("MEDIA:"):]

    # Get the directory and base filename without extension
    directory = os.path.dirname(input_mp3_path)
    base_filename = os.path.splitext(os.path.basename(input_mp3_path))[0]

    # Construct the output OGG path
    output_ogg_path = os.path.join(directory, f"{base_filename}.ogg")

    # Construct the ffmpeg command
    command = f"ffmpeg -i {input_mp3_path} -c:a libopus -b:a 32k -ar 48000 -ac 1 {output_ogg_path}"

    print(f"Executing command: {command}")
    os.system(command)
    print(output_ogg_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python convert_mp3_to_ogg.py <input_mp3_path>")
        sys.exit(1)
    
    input_mp3_file = sys.argv[1]
    convert_mp3_to_ogg(input_mp3_file)
