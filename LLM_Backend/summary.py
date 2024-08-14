import torch
from transformers import AutoTokenizer
from transformers import AutoModelForSeq2SeqLM

def get_summary(article_text):


    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f'Using {device} device')

    model_checkpoint = "csebuetnlp/mT5_multilingual_XLSum"
    tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_checkpoint)
    model = model.to(device)

    input_ids = tokenizer(
        article_text,
        return_tensors="pt",
        truncation=True,
        max_length=2048
    )
    generated_tokens = model.generate(
        input_ids["input_ids"],
        attention_mask=input_ids["attention_mask"],
        max_length=64,
        no_repeat_ngram_size=2,
        num_beams=4
    )
    summary = tokenizer.decode(
        generated_tokens[0],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False
    )
    return(summary)