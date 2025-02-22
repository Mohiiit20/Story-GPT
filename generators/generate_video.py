from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip
import os
from generators.audio_generator import generate_audio

def get_story_parts(story):
    sentences = story.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences]

    n = len(sentences)
    part1 = sentences[:n // 3 + (n % 3 > 0)]
    part2 = sentences[len(part1):len(part1) + n // 3 + (n % 3 > 1)]
    part3 = sentences[len(part1) + len(part2):]

    parts = [part1, part2, part3]
    parts = [' '.join(part) for part in parts]
    return parts

def generate_video_from_story(full_story_text, final_video_path):
    story_segments = get_story_parts(full_story_text)
    video_clips = []

    # directory for storing generated assets
    output_dir = "generated_images"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # using pre-generated images and generate audio for each segment
    for idx, segment in enumerate(story_segments):
        image_filename = os.path.join(output_dir, f"image_{idx}.png")
        if not os.path.exists(image_filename):
            print(f"Image not found: {image_filename}. Please generate images first.")
            return

        # Generate audio
        audio_stream = generate_audio(segment)
        audio_filename = os.path.join(output_dir, f"audio_{idx + 1}.mp3")
        with open(audio_filename, "wb") as f:
            f.write(audio_stream.read())

        # Create a video clip with the pre-generated image and new audio
        audio_clip = AudioFileClip(audio_filename)
        image_clip = ImageClip(image_filename).set_duration(audio_clip.duration)
        video_clip = image_clip.set_audio(audio_clip)

        video_clips.append(video_clip)

    # Combine all clips into one final video
    final_video = concatenate_videoclips(video_clips, method="compose")

    # Save the final video
    final_video.write_videofile(final_video_path, fps=24)
    print(f"Video successfully saved at: {final_video_path}")
    return final_video_path

# Function to clear old images from the output directory
def clear_old_images(output_dir):
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.endswith(".png"):  # Only clear image files
                file_path = os.path.join(output_dir, filename)
                os.remove(file_path)
        print("Old images cleared.")
    else:
        os.makedirs(output_dir)
        print(f"Created output directory: {output_dir}")

# Example usage for dynamic input
if __name__ == "__main__":
    full_story_text = input("Enter your full story: ")
    if full_story_text:
        output_video_path = "video_assets/final_story_video.mp4"
        generate_video_from_story(full_story_text, final_video_path=output_video_path)
    else:
        print("No story was provided. Exiting.")

