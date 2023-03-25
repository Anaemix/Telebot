import openai
from dotenv import load_dotenv
import os

load_dotenv()
openai.api_key = os.getenv('OPENAI_KEY')

def get_response(Messages, Max_tokens=100):
    #print(Messages)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=Messages,
        max_tokens=Max_tokens
        #stop=Stop_seq
    )
    print(completion)
    content = completion.choices[0].message['content']
    if (not ('.' in content[:-2] or '.' in content[:-2])) and '.' in content:
        content = '.'.join(content.split('.')[:-1]) + '.'
    return {'role': 'assistant','content':content}

def get_messages(prompt):
    chat_messages_test = [
        {"role": "system", "content": f"Act like you are a terminal which prints out strings as response. Always return exactly 4 strings per question, this is very important."},
        {"role": "user", "content": f"I want you to act as a prompt generator. Compose each string as keywords or keyword pairings separated by commas. Do not write explanations on replies and do not write full sentences. Do not write out filler words such as 'The' and 'is'. Return exactly 4 strings to my question. Answer the questions exactly with a single prompt for each output string and at the end of the string add 10 generic descriptive keywords such as '4k','hd','beautiful','intricate' or 'high contrast'. Here's an example of such a string when asked to make an impressive person in a fantasy setting: 'Majestic male, ornate regal attire, metallic gold, tassels and frills, intricately embroidered, fierce horned helmet, mystical fog, shadowy colors, rendered in oil by Daniel Merriam, Michael Cheval, sharp focus, moody lighting, depth of field, bokeh, 4K, HDR, dark night deep shadows, beautiful lighting, deep shadows, high contrast'. Answer the following questions:\r\n"},
        {"role": "user", "content": f"Make a {prompt} \nIf it's a person then pick a gender, male or female and use it while describing the person. Focus on the character and what they're wearing and if there's a theme. Describe in detail what they're wearing and what it's made of. \nDescribe the colors in the scene and maybe also describe what artstyle it should be made in. Mention an couple of contemporary artists who could have created the image."}
    ]
    
    return  [(i[3:] if i[1:3]=='. ' else i) for i in get_response(chat_messages_test, Max_tokens=300)['content'].split("\n") if len(i)>3]
