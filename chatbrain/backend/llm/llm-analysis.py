from openai import OpenAI
from dotenv import load_dotenv
import os
import deepseek_v2_tokenizer as dtok

load_dotenv()  # Load environment variables from .env file
model_name = os.getenv("MODEL_NAME")
base_url = os.getenv("BASE_URL")

# usage stats : https://platform.deepseek.com/usage
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url=base_url)

def calculate_api_cost(chat_completion):
    # Pricing information
    input_price_cache_hit = 0.014  # $0.014 per 1M tokens (cache hit)
    input_price_cache_miss = 0.14  # $0.14 per 1M tokens (cache miss)
    output_price = 0.28  # $0.28 per 1M tokens

    # Extract token usage details from the ChatCompletion object
    usage = chat_completion.usage
    prompt_tokens = usage.prompt_tokens
    completion_tokens = usage.completion_tokens
    prompt_cache_hit_tokens = usage.prompt_cache_hit_tokens
    prompt_cache_miss_tokens = usage.prompt_cache_miss_tokens

    # Calculate input cost based on cache hit/miss
    input_cost_cache_hit = (prompt_cache_hit_tokens / 1_000_000) * input_price_cache_hit
    input_cost_cache_miss = (prompt_cache_miss_tokens / 1_000_000) * input_price_cache_miss
    total_input_cost = input_cost_cache_hit + input_cost_cache_miss

    # Calculate output cost
    total_output_cost = (completion_tokens / 1_000_000) * output_price

    # Total cost
    total_cost = total_input_cost + total_output_cost

    return total_cost


def getSystemPrompt(user1_name, user2_name, user1_nickname, user2_nickname):
    return f"""
      You are an advanced conversation analyst. Analyze the following chat between:
      1) {user1_name} (nickname: {user1_nickname})
      2) {user2_name} (nickname: {user2_nickname})

      Your task is to provide a detailed analysis with the following metrics:

      1) **Conversation-level metrics:**
        - **Stability Score (out of 100):** Reflects the emotional consistency and lack of dramatic fluctuations in the conversation.
        - **Health Score (out of 100):** Indicates the overall positive or negative tone and supportiveness of the conversation.
        - **Intensity Score (out of 100):** Measures the engagement level, such as message frequency and response speed.

      2) **User-level metrics (for each user by name):**
        - **Assertiveness (out of 100):** The extent to which the user expresses their opinions and stands firm on their views.
        - **Positiveness (out of 100):** The level of positive emotions and optimism expressed by the user.
        - **Affection Towards the Other (out of 100):** Signs of warmth, care, or fondness directed at the other person.
        - **Romantic Attraction Towards the Other (out of 100):** Indicators of romantic interest or desire towards the other person.
        - **Rationality (out of 100):** The degree to which the user thinks logically and objectively.
        - **Emotiveness (out of 100):** The overall expression of emotions by the user.
        - **IQ Estimate (integer):** A rough estimate of the user's intelligence based on language use and reasoning in the conversation.

      3) **Insights:**
        - An array of at least three insights IN THE SAME LANGUAGE AS THE MESSAGES (if they are predominantly in one message, in english otherwise)
        of around 50 words each, offering deeper interpretation of the conversation. These should be analysis or inferences that the participants 
        may not be aware of or may find valuable.

      IMPOSED OUTPUT JSON FORMAT: 

      {{
        "conversation_metrics": {{
        "stability_score_out_of_100": int,
        "health_score_out_of_100": int,
        "intensity_score_out_of_100": int
        }},
        "users": {{
        "{user1_name}": {{
          "assertiveness": int,
          "positiveness": int,
          "affection_towards_other": int,
          "romantic_attraction_towards_other": int,
          "rationality": int,
          "emotiveness": int,
          "IQ_estimate": int
        }},
        "{user2_name}": {{
          "assertiveness": int,
          "positiveness": int,
          "affection_towards_other": int,
          "romantic_attraction_towards_other": int,
          "rationality": int,
          "emotiveness": int,
          "IQ_estimate": int
        }}
        }},
        "insights": ["Insight 1", "Insight 2", "Insight 3"]
      }}
    """

def promptToJSON(prompt, maxOutputTokens, model_name,
                  user1_name, user2_name, user1_nickname, user2_nickname):
    # build the system prompt
    systemPrompt = getSystemPrompt(user1_name, user2_name, user1_nickname, user2_nickname)

    #check for outsanding prices, get general token information
    price, tokenCount = dtok.apiCallPrice(prompt + systemPrompt, maxOutputTokens, model_name)
    if price > 0.001:
        print(f"Warning: This API call will cost ${price:.2f} USD.")
        return None
    print(f"Token count: {tokenCount}")
    print(f"Calculated API call price: ${price:.8f} USD")

    # make the API call
    response = api_call("deepseek-chat", maxOutputTokens, systemPrompt, prompt)
    if response.choices[0].message.refusal != None:
        print("Model refused to answer for the following reason:")
        print(response.choices[0].message.refusal)
        return None

    # print result data
    print(f"API call price: ${calculate_api_cost(response):.8f} USD")
    print(f"Total tokens used: {response.usage.total_tokens}")
    print(f"Prompt cached tokens: {response.usage.prompt_cache_hit_tokens}")
    print(f"Prompt uncached tokens: {response.usage.prompt_cache_miss_tokens}")
    print(f"Completion tokens: {response.usage.completion_tokens}")
    print(f"--------------------\n")
    print("JSON output:")
    jsonOutput = response.choices[0].message.content
    print(jsonOutput)
    return jsonOutput, response

def api_call (model, maxOutputTokens=2000, systemPrompt=None, userPrompt=None):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": systemPrompt},
            {"role": "user", "content": userPrompt}
        ],
        max_tokens=maxOutputTokens,
        response_format={'type': 'json_object'}
    )
    return response

def llm_analysis(file_path: str, user1_name: str, user2_name: str, 
                user1_nickname: str, user2_nickname: str):
    return None

if __name__ == "__main__":
    def get_string_from_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()
    jsonOutput, response = promptToJSON(get_string_from_file("../data/shrink_test_output.txt"), 1500, model_name, "Joey", "Norma", "J", "N")
    #save the ChatCompletion object to a file
    with open("chat_completion.json", "w") as f:
        f.write(str(response))
    print(response)