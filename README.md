# Using GPT to chat with HERE's discover endpoint

## Blog posts

There are two blog posts published on HERE's developer blog that explain this project in more detail:
* https://www.here.com/learn/blog/chatwithgs7-powering-location-queries-with-here-gs7-and-openai
* https://www.here.com/learn/blog/chatwithgs7-enabling-the-front-end-experience

  


## Prerequisites

OPENAI_API_KEY and HERE_API_KEY need to be set in environment variables.

## What does the script do?

For a user question like 

    "In which districts in Berlin are streets named Kastanienallee?"

the script uses GPT to create an API call like

    https://discover.search.hereapi.com/v1/discover?at=52.5200,13.4050&q=Kastanienallee%20Berlin

Based on the API response, GPT is then used to create a response like the following:

    "Streets named Kastanienallee can be found in the following districts in Berlin: Prenzlauer Berg, Rosenthal, Hellersdorf, Westend, and Blankenburg."
