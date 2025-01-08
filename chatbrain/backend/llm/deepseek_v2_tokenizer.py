# pip3 install transformers
# python3 deepseek_v2_tokenizer.py
import transformers

def tokenCount(text, chat_tokenizer_dir):
        """Returns the number of tokens in `text`, based on the tokenizer in `chat_tokenizer_dir`."""
        tokenizer = transformers.AutoTokenizer.from_pretrained( 
                chat_tokenizer_dir, trust_remote_code=True
                )
        return len(tokenizer.encode(text))

def tokenList(text, chat_tokenizer_dir):
        """Returns the list of tokens in `text`, based on the tokenizer in `chat_tokenizer_dir`."""
        tokenizer = transformers.AutoTokenizer.from_pretrained(
                chat_tokenizer_dir, trust_remote_code=True
                )
        return tokenizer.encode(text)

def apiCallPrice(text, outputSize, chat_tokenizer_dir, imageCount=0, imageSizes=[]):
        """Returns the price of an API call to `deepseek-ai/DeepSeek-V3` for `text`, given a specific `outputSize`."""
        # assuming deepseek-ai/DeepSeek-V3 usage
        price_per_M_tokens = 0.1 # in USD
        tokens = tokenCount(text, chat_tokenizer_dir) + outputSize
        return tokens * price_per_M_tokens / 1e6, tokenCount(text, chat_tokenizer_dir)

if __name__ == "__main__":
        chat_tokenizer_dir = "deepseek-ai/DeepSeek-V3"
        text = """
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
        - An array of at least three insights offering deeper interpretation of the conversation. These should be analysis or inferences that the participants may not be aware of or may find valuable.

      Ensure that the output is strictly in JSON format with the following structure:

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

      Conversation:
      {conversation_text}
    """
        print("Token count: " + str(tokenCount(text, chat_tokenizer_dir)))
        tokens = tokenList(text, chat_tokenizer_dir)
        print("Token list: ")
        print(tokens)
        print("API call price: {:.8f} USD".format(apiCallPrice(text, 1500, chat_tokenizer_dir)))