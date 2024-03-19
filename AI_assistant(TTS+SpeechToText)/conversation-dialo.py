from transformers import TFGPT2LMHeadModel, GPT2Tokenizer

# Load the DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-medium"
model = TFGPT2LMHeadModel.from_pretrained(model_name)
tokenizer = GPT2Tokenizer.from_pretrained(model_name)

# Define a conversation
conversation = ["User: Hello, how are you?", "Assistant:"]

# Encode the conversation
inputs = tokenizer.encode("\n".join(conversation), return_tensors="tf")

# Generate a response
output = model.generate(inputs, max_length=150, num_return_sequences=1, no_repeat_ngram_size=2)
response = tokenizer.decode(output[0], skip_special_tokens=True)

print(response)
