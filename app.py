import streamlit as st
import openai
from tiktoken import encoding_for_model



def generate_email(rawmail, tomail,lengthmail,tonemail):
  
  response = openai.ChatCompletion.create(
      model="gpt-4o",
      temperature = 0.4,
      messages=[
          {
              "role":
              "system",
              "content":
              """"You are an email writing expert. You help users write emails for specific situations.You consider these 4 inputs from the user:
              1. The content of the email which the user will give.
              2. The person who you are sending this mail to.
              3. The length of the mail
              4. The tone of the email, which the user will give.
              You need to form the email in a proper manner and in accordance with the situation.Dont use too much of the same pronouns or words.You will get high reward for achieving the best possible output. 
             """
          },
          {
              "role": "user",
              "content": f"""1.Content : {rawmail}\n
                             2. Mail sent to: {tomail}\n
                             3. Length of mail: {lengthmail}\n
                             4. Tone   : {tonemail}
"""
          },
      ],
  )
  generated_questions = response['choices'][0]['message']['content']
  return generated_questions


# Function to count tokens in a string
def count_tokens(text):
    encoding = encoding_for_model("gpt-4o")  # Use appropriate encoding for your model
    return len(encoding.encode(text))

# Main Streamlit App
def main():
    st.title("Email Generator")

    # Collapsible Sidebar for OpenAI Key Input
    with st.sidebar:
        st.header("OpenAI API Key")
        api_key = st.text_input("Paste your OpenAI API key here:", type="password")  # Hide input
        if api_key:
            openai.api_key = api_key
        else:
            st.warning("Please enter your OpenAI API key.")
        token_count_placeholder = st.empty()
        cost_usd_placeholder = st.empty()
        cost_inr_placeholder = st.empty()

    # User Input (unchanged)
    rawmail = st.text_area("I want to write an email about...", height=150)
    tomail = st.text_area("I am sending this email to...")
    lengthmail = st.selectbox(
        "The length of this email should be...",
        ["Short(few line(s))", "Brief(1 to 2 Paras)", "Proper(Multiple Paras)", "Detailed(Long and properly explained)","Custom(as per the content)"]
    )
    tonemail = st.selectbox(
        "The tone of this email should be...",
        ["Professional", "Friendly", "Urgent", "Enthusiastic", "Formal"]
    )
    

    # Generate Button
    if st.button("Generate Email"):
        if rawmail and tonemail and openai.api_key:  # Check if API key is set
            with st.spinner("Generating..."):
                email = generate_email(rawmail, tomail,lengthmail,tonemail)
                st.subheader("Your Email:")
                st.code(email, language="text")
                
                prompt_tokens = count_tokens(f"""
                                             You are an email writing expert. You help users write emails for specific situations.You consider these 4 inputs from the user:
              1. The content of the email which the user will give.
              2. The person who you are sending this mail to.
              3. The length of the mail
              4. The tone of the email, which the user will give.
              You need to form the email in a proper manner and in accordance with the situation.Dont use too much of the same pronouns or words.You will get high reward for achieving the best possible output.
                                        1.Content : {rawmail}\n
                             2. Mail sent to: {tomail}\n
                             3. Length of mail: {lengthmail}\n
                             4. Tone   : {tonemail}     
                                             """)
                completion_tokens = count_tokens(email)
                total_tokens = prompt_tokens + completion_tokens
                
                # Estimated Cost (adjust these prices as needed)
                price_per_1k_tokens = 0.01  # USD price per 1,000 tokens
                cost_usd = (total_tokens / 1000) * price_per_1k_tokens
                usd_to_inr = 83.72  # Approximate conversion rate
                cost_inr = cost_usd * usd_to_inr
                token_count_placeholder.write(f"**Token Usage:** {total_tokens} tokens")
                cost_usd_placeholder.write(f"**Estimated Cost (USD):** ${cost_usd:.4f}")
                cost_inr_placeholder.write(f"**Estimated Cost (INR):** Rs. {cost_inr:.2f}")

        else:
            if not openai.api_key:
                st.warning("Please enter your OpenAI API key.")
            else:
                st.warning("Please fill in all fields.")


if __name__ == "__main__":
    main()
