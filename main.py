import os
import requests
from openai import OpenAI

# Instructions for GTP to transform the user query to an API call
system_instructions_1 = "Translate the user prompt to a full API call to HERE's discover endpoint " \
                        "(https://discover.search.hereapi.com/v1/discover). " \
                        "Make sure to include the at and q parameter, but omit the apiKey parameter. " \
                        "Remember that the at parameter should contain coordinates. " \
                        "Your response should only contain the API call, in one line and nothing else."

# Instructions for GTP to transform the API response to a natural language response
system_instructions_2 = "Create an informative and helpful English prompt suitable for a TTS that answers the user " \
                        "question '#1#' solemnly based on the JSON object that is provided. " \
                        "The prompt should be a direct answer to the question." \
                        "(The JSON is a response from https://discover.search.hereapi.com/v1/discover). " \
                        "Do not mention JSON or that the information is from a JSON object."

# the user query
user_query = "In which districts in Berlin are streets named Kastanienallee?"


# Call HERE's discover endpoint and returns the JSON result.
# Fixes a few common issue's with the API call created by GTP, if they are present.
def call_here_discover_endpoint(call_string):
    if call_string.startswith("GET "):
        call_string = call_string[4:]
    if call_string.endswith("&apiKey=YOUR_API_KEY"):
        call_string = call_string[:len(call_string) - 20]
    if call_string.endswith("&apiKey={YOUR_API_KEY}"):
        call_string = call_string[:len(call_string) - 22]
    if call_string.startswith("/v1/discover"):
        call_string = "https://discover.search.hereapi.com" + call_string
    call_string += "&apiKey=" + os.environ.get("HERE_API_KEY")
    response = requests.get(call_string)
    #print(json.dumps(response.json(), indent=2))
    return response.json()


# Simplifies the HERE API response. Removes some JSON fields, so that GTP focuses on what's important.
def simplify_discover_result(response):
    for item in response.get("items", []):
        item.pop("id")
        item.pop("language")
        item.pop("position")
        item.pop("distance")
        if "mapView" in item:
            item.pop("mapView")
        if "access" in item:
            item.pop("access")
        if "contacts" in item:
            item.pop("contacts")
        if "openingHours" in item:
            item.pop("openingHours")
        if "payment" in item:
            item.pop("payment")


open_AI_client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Create an API call based on the user question
chat_completion_1 = open_AI_client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_instructions_1,
        },
        {
            "role": "user",
            "content": user_query,
        }
    ],
    model="gpt-3.5-turbo",
)
discover_query = chat_completion_1.choices[0].message.content
discover_result = call_here_discover_endpoint(discover_query)

# Create a natural language response based on the JSON result from the API
simplify_discover_result(discover_result)
discover_result = str(discover_result)[0:3500]
system_instructions_2 = system_instructions_2.replace("#1#", user_query)
chat_completion_2 = open_AI_client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": system_instructions_2,
        },
        {
            "role": "user",
            "content": discover_result,
        }
    ],
    model="gpt-3.5-turbo",
)

# Print the results
response_2 = chat_completion_2.choices[0].message.content
print(user_query)
print(discover_query)
print(response_2)
