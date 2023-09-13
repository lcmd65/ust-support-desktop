
import transformers
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

token_ = "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"
token_write = "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"
tokenizer = AutoTokenizer.from_pretrained("tiiuae/falcon-180B", token = token_)
model = AutoModelForCausalLM.from_pretrained("tiiuae/falcon-180B", token = token_)

pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    torch_dtype=torch.bfloat16,
    trust_remote_code=True,
    device_map="auto",
)

sequences = pipeline(
   "Xin chào, cho tôi xin thông tin chương trình đào tạo của hcmus",
    max_length=200,
    do_sample=True,
    top_k=10,
    num_return_sequences=1,
    eos_token_id=tokenizer.eos_token_id,
)

for seq in sequences:
    print(f"Result: {seq['generated_text']}")