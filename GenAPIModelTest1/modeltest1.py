from transformers import AutoModelForCausalLM, AutoTokenizer, AutoModel
import torch

def print_dict(**kwargs):
    print("Keys = ", kwargs.keys())
    print("Values = ", kwargs.values())
    return kwargs

model_name = "gpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
modelLLM = AutoModelForCausalLM.from_pretrained(model_name, is_decoder=True)


modelLLM.eval()

input_Text = "data science is a field that focuses on the analysis of data"
input_Ids = tokenizer.encode(input_Text, return_tensors='pt')

print(input_Ids)

attention_mask = torch.ones(input_Ids.shape, dtype=torch.long)
with torch.no_grad():  # Disable gradient calculation
    output = modelLLM.generate(
        input_Ids,
        attention_mask=attention_mask,
        max_length=50,
        num_return_sequences=1,
        pad_token_id=tokenizer.eos_token_id  # Set pad_token_id to eos_token_id
    )
#
#genText = tokenizer.decode(output[0], skip_special_tokens=True)
#print("Generated Text = ", genText)


## Generating Emdebings

model_name = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
modelLLM = AutoModel.from_pretrained(model_name)

inputs = tokenizer("Jai Mataji", return_tensors="pt", padding=True, truncation=True)
#outputs = modelLLM(**inputs)
#embedding = outputs.last_hidden_state.mean(dim=1).detach().numpy()
#
#print("Embedding = ", embedding)*/


print_dict(**inputs)




