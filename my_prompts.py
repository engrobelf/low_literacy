file_map = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Act as a low literacy expert and please provide a cohesive summary of the following section excerpt for people with low literacy,
focusing on the key points and main ideas, while maintaining clarity and conciseness and low complexity.

'''{text}'''

FULL SUMMARY:
"""


file_combine = """
Read all the provided summaries from a larger document. They will be enclosed in triple backticks. 
Language Adjustment: Summarize in Dutch if the original letter is in Dutch, and in English if the letter is in English.
Summarize the document focusing on the following structure:


    📩 Sender: Use an emoji to visually represent the sender for quick understanding. Provide the name or organization of the sender in this section separately.

    🎯 Purpose: Briefly describe the main purpose or topic of the letter in a simple sentence or phrase, using an emoji if possible for visual emphasis.

    🔑 Core Message or Actions Required:

        For specific actions needed from the recipient, label these as "🎯 Action Points" and use emojis for each. Keep explanations concise, aiming for a maximum of 6 words per action point for simplicity.
        For informative content without required actions, refer to these as "💡 Highlights," following the same brevity and emoji usage.

    📞 Contact Information: Provide a brief summary of given contact details. If absent, clearly state "🚫 No contact details provided." If specific actions such as vaccination are mentioned or advice is needed, suggest contacting healthcare providers, local health departments (GGD in the Netherlands), or another relevant organization for the most current advice and instructions.

    📍 Call to Action & Address:

        Summarize specific call to action in 6 words (excluding links and phone numbers).
        Include relevant dates, deadlines, or addresses succinctly.

    📌 Approach: Maintain a focus on the essentials, using minimal wording and excluding unrelated information for clarity and brevity.
 

'''{text}'''


"""

youtube_map = """
You will be given a single section from a transcript of a youtube video. This will be enclosed in triple backticks.
Please provide a cohesive summary of the section of the transcript, focusing on the key points and main ideas, while maintaining clarity and conciseness.

'''{text}'''

FULL SUMMARY:
"""


youtube_combine = """
Read all the provided summaries from a youtube transcript. They will be enclosed in triple backticks.
Determine what the overall video is about and summarize it with this information in mind. 
Synthesize the info into a well-formatted easy-to-read synopsis, structured like an essay that summarizes them cohesively. 
Do not simply reword the provided text. Do not copy the structure from the provided text.
Avoid repetition. Connect all the ideas together.
Preceding the synopsis, write a short, bullet form list of key takeaways.
Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented. 

'''{text}'''


"""