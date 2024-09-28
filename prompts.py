from langchain.prompts import FewShotPromptTemplate, PromptTemplate

# Define examples for the story
# examples = [
#     {
#         "topic": "Waiting for My Turn",
#         "story": "Alex sometimes has to wait his turn to play. While waiting, he watches his friends and stays patient. When it's his turn, he gets excited but remembers to play nicely. Waiting can be hard, but Alex knows everyone gets a turn."
#     },
#     {
#         "topic": "Asking for Help",
#         "story": "Ethan sometimes feels stuck when he doesn't know what to do. Instead of getting upset, he asks his teacher or a friend for help. Ethan learns that asking for help is a good way to solve problems quickly."
#     },
#     {
#         "topic": "Brushing My Teeth",
#         "story": "Lily brushes her teeth every morning and night to keep them healthy. She uses her toothbrush, toothpaste, and water to clean her teeth. When she finishes, her mouth feels fresh and clean, and Lily smiles brightly."
#     }
# ]
#
# # Create story generation prompt templates
# example_prompt = PromptTemplate(
#     input_variables=["topic", "story"],
#     template="User: {topic}\nAI: {story}"
# )
#
# prefix = (
#     "Generate a story on the topic '{topic}' in about 50 words. "
#     "The story must be written in third person, like the examples provided. "
#     "Do not use first-person language such as 'I', 'me', or 'my'. "
#     "The story should describe what a specific child (e.g., Alex, Ethan, Lily) does. "
#     "The story must teach social skills and manners related to the topic for children with ASD. "
#     "Keep the story simple and easy to understand for children aged 5-10."
# )
#
# suffix = "User: {topic}\nAI: "
#
# few_shot_prompt_template = FewShotPromptTemplate(
#     examples=examples,
#     example_prompt=example_prompt,
#     prefix=prefix,
#     suffix=suffix,
#     input_variables=["topic"],
#     example_separator="\n"
# )

# Image prompt examples
examples_image = [
    {
        "story": "Alex sometimes has to wait his turn to play. While waiting, he watches his friends and stays patient. When it's his turn, he gets excited but remembers to play nicely.",
        "prompt": "A patient and excited boy waiting his turn to play with friends, smiling as he watches them. He plays nicely when it's his turn."
    },
    {
        "story": "Ethan sometimes feels stuck when he doesn't know what to do. Instead of getting upset, he asks his teacher or a friend for help.",
        "prompt": "A confused boy raising his hand to ask for help from a nearby teacher in a classroom. The teacher approaches to assist calmly."
    },
    {
        "story": "Lily brushes her teeth every morning and night to keep them healthy.",
        "prompt": "A girl smiling in front of a mirror while brushing her teeth in a clean bathroom with a cup of water beside her."
    }
]

example_prompt_image = PromptTemplate(
    input_variables=["story"],
    template="{story} this is a story I want to generate an image for. Give me a detailed prompt for an image generation model. Address the gender of the child, but do not use their name."
)

prefix_image = (
    "Below are examples of stories and their corresponding image generation prompts. "
    "For each new story, create a concise image generation prompt focused on key visual details. "
    "Use 'boy' or 'girl' to refer to the child instead of using their name."
)

suffix_image = "User: {story}\nAI:"

few_shot_prompt_template_image = FewShotPromptTemplate(
    examples=examples_image,
    example_prompt=example_prompt_image,
    prefix=prefix_image,
    suffix=suffix_image,
    input_variables=["story"],
    example_separator="\n"
)

# Function to split story into two parts
def get_story_list(story):
    sentences = story.split('.')
    sentences = [s.strip() for s in sentences if s.strip()]
    sentences = [s + '.' for s in sentences]
    n = len(sentences) // 2
    return [" ".join(sentences[:n]), " ".join(sentences[n:])]
