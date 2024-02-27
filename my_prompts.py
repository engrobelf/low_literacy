file_map = """
You will be given a single section from a text. This will be enclosed in triple backticks.
Act as a low literacy expert and please provide a cohesive summary of the following section excerpt for people with low literacy,
focusing on the key points and main ideas, while maintaining clarity and conciseness and low complexity.

'''{text}'''

FULL SUMMARY:
"""


file_combine = """
Read all the provided summaries from a larger document. They will be enclosed in triple backticks. 
Summarize the document focusing on the following structure:
 
1. State the organization or sender with an emoji.
2. Summary: Summarize the document in a couple sentence that can be understood by people with low literacy level. I prefer the
summary to be very straightforward, with each action point and piece of information separated clearly and presented with minimal words for clarity.
Preceding the synopsis, write a short, bullet form list of key action with the corresponding deadlines associated if applicable.
Format in HTML. Text should be divided into paragraphs. Paragraphs should be indented.

3. Key actions: List the key actions briefly with emojis for each point, tailored for a primary school understanding level.
If applicable add the deadlines associated with the expected actions.
3. Concisely provide the contact information and location if applicable
4. If there is no contact information then you can say " there is no contact information"
 

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