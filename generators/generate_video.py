from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips
from generators.generate_image import generate_image
from generators.audio_generator import generate_audio
import tempfile

def split_story(story, max_words=30):
    words = story.split()
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]

def generate_video_from_story(story, output_path="final_story_video.mp4"):
    story_segments = split_story(story)
    video_clips = []

    for idx, segment in enumerate(story_segments):
        # Generate image
        image = generate_image(segment)
        if image is None:
            print(f"Image generation failed for segment {idx+1}. Skipping...")
            continue

        # Save the generated image temporarily
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as img_file:
            image.save(img_file.name)
            image_path = img_file.name

        # Generate audio
        audio_stream = generate_audio(segment)
        if audio_stream is None:
            print(f"Audio generation failed for segment {idx+1}. Skipping...")
            continue

        # Save audio temporarily
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as audio_file:
            audio_file.write(audio_stream.read())
            audio_file_path = audio_file.name

        # Create video clip
        audio_clip = AudioFileClip(audio_file_path)
        image_clip = ImageClip(image_path).set_duration(audio_clip.duration).set_fps(24)
        image_clip = image_clip.set_audio(audio_clip)

        video_clips.append(image_clip)

    if not video_clips:
        print("No video clips were generated.")
        return

    # Concatenate all clips
    final_video = concatenate_videoclips(video_clips, method="compose")
    final_video.write_videofile(output_path, fps=24)
    print(f"Video successfully saved to {output_path}")

# Example usage
if __name__ == "__main__":
    story_text = input("Enter your story prompt: ")
    generate_video_from_story(story_text)
