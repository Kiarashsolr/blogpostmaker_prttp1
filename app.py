import streamlit as st
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Get the OpenAI API key and passcode from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')
APP_PASSCODE = os.getenv('APP_PASSCODE')

# Function to generate skeleton/summary of the blogpost using OpenAI API
def generate_skeleton(field_of_work, example_posts):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a capable chatbot that takes in the \"field of work\", and returns a skeleton/summary of a blogpost that such a business would put into their website. "
                        "The output that you give will be displayed in a field for the user to modify, and then it will be shown to another agent so that it can be turned into a complete blogpost. "
                        "***Very important: You are a piece of a bigger program, and so it is crucial that you respond as it is expected from you. try your best to respond, and if you cannot, respond with \"error\"***\n\n"
                        "here are some guidelines that might be helpful: \n\n"
                        "You are a skilled blog writer tasked with creating an engaging article based on a few key words. Your goal is to craft a compelling piece that fits the style and tone of the given magazine while incorporating the provided parameters naturally.\n"
                        "Here's the information you'll be working with:\n"
                        "Work Field:  (it will be sent to you as a message)\n"
                        "Follow these guidelines to create your article:\n"
                        "1. Structure: Begin with an attention-grabbing headline, followed by an introductory paragraph, 3-4 main body paragraphs, and a conclusion.\n"
                        "2. Content: Incorporate all the provided keywords into your article. Ensure they flow naturally within the context of your writing.\n"
                        "3. Research: While you shouldn't cite specific sources, feel free to include relevant facts, statistics, or anecdotes that support your article's theme.\n"
                        "5. Creativity: Use your imagination to create an interesting narrative or angle that ties the keywords together in an unexpected or insightful way.\n"
                        "Remember, your goal is to create an engaging and informative article that seamlessly incorporates the given keywords while matching the style and tone of the specified magazine."
                    )
                },
                {
                    "role": "user",
                    "content": field_of_work
                }
            ],
            temperature=1,
            max_tokens=2171,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Function to generate the raw blogpost from skeleton/summary
def makeRawBlogpost(skeleton):
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a skilled blog writer tasked with creating an engaging article based on the skeleton that is provided to you. "
                        "***Very important: You are a piece of a bigger program, and so it is crucial that you respond as it is expected from you. try your best to respond, and if you cannot, respond with \"error\"***\n\n"
                        "Here are some guidelines that might be helpful: \n\n"
                        "You are a skilled blog writer tasked with creating an engaging article based on a few key words. Your goal is to craft a compelling piece that fits the style and tone of the given magazine while incorporating the provided parameters naturally.\n"
                        "Here's the information you'll be working with:\n"
                        "Skeleton/summary of the desired blog post.\n"
                        "Follow these guidelines to create your article:\n"
                        "1. Structure: Begin with an attention-grabbing headline, followed by an introductory paragraph, 3-4 main body paragraphs, and a conclusion.\n"
                        "2. Content: Incorporate all the provided keywords into your article. Ensure they flow naturally within the context of your writing.\n"
                        "3. Research: While you shouldn't cite specific sources, feel free to include relevant facts, statistics, or anecdotes that support your article's theme.\n"
                        "5. Creativity: Use your imagination to create an interesting narrative or angle that ties the keywords together in an unexpected or insightful way.\n"
                        "Remember, your goal is to create an engaging and informative article that seamlessly incorporates the given keywords while matching the style and tone of the specified magazine."
                    )
                },
                {
                    "role": "user",
                    "content": skeleton
                }
            ],
            temperature=1,
            max_tokens=3516,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Function to generate Joe Guay style blogpost
def generate_joe_guay_blogpost(skeleton):
    try:
        raw_blogpost = makeRawBlogpost(skeleton)
        response = openai.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:vdidopenai:author-style-joe:9hjTUH3a",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI agent trained by AICO, and you can rewrite the AI written text sent to you in the style of author Joe Guay."
                    )
                },
                {
                    "role": "user",
                    "content": raw_blogpost
                }
            ],
            temperature=0.95,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Function to generate Shankar Narayan style blogpost
def generate_shankar_narayan_blogpost(skeleton):
    try:
        raw_blogpost = makeRawBlogpost(skeleton)
        response = openai.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:vdidopenai:author-style-shank:9hjAJh7P",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an AI agent trained by AICO, and you can rewrite the AI written text sent to you in the style of author Shankar Narayan."
                    )
                },
                {
                    "role": "user",
                    "content": raw_blogpost
                }
            ],
            temperature=0.95,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"

# Function to generate AI-written blogpost
def generate_ai_written_blogpost(skeleton):
    return makeRawBlogpost(skeleton)

# Streamlit app
def main():
    st.title("AI-Based Blogpost Writer")

    # Authentication step
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        passcode = st.text_input("Enter Passcode", type="password")
        if st.button("Authenticate"):
            if passcode == APP_PASSCODE:
                st.session_state.authenticated = True
                st.experimental_rerun()
            else:
                st.error("Incorrect passcode. Please try again.")
        return

    st.header("Input Section")

    st.subheader("Material")
    field_of_work = st.text_input("Field of Work")
    example_posts = st.text_area("Example Blogposts")

    if st.button("Generate Skeleton/Summary of the Blogpost"):
        # Call the generate_skeleton function
        skeleton = generate_skeleton(field_of_work, example_posts)
        st.session_state.skeleton = skeleton

    # Show the skeleton/summary if it has been generated
    if 'skeleton' in st.session_state:
        st.text_area("Skeleton/Summary of the Blogpost", st.session_state.skeleton, height=200)

    st.subheader("Tone")
    tone = st.radio(
        "Select a tone:",
        ("Joe Guay", "Shankar Narayan", "AI written")
    )

    st.header("Generated Blogpost")
    if st.button("Generate Blogpost"):
        # Check if the skeleton/summary exists and use it to generate the blog post
        if 'skeleton' in st.session_state:
            skeleton = st.session_state.skeleton

            # Generate blog post based on the selected tone
            if tone == "Joe Guay":
                blogpost = generate_joe_guay_blogpost(skeleton)
            elif tone == "Shankar Narayan":
                blogpost = generate_shankar_narayan_blogpost(skeleton)
            elif tone == "AI written":
                blogpost = generate_ai_written_blogpost(skeleton)

            st.session_state.blogpost = blogpost

    # Show the final blogpost if it has been generated
    if 'blogpost' in st.session_state:
        st.text_area("Blogpost", st.session_state.blogpost, height=300)

if __name__ == "__main__":
    main()
