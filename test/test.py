
def questionAnswering(question_, context_):
    from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
    # Load the question answering model and tokenizer
    model = AutoModelForQuestionAnswering.from_pretrained("ancs21/xlm-roberta-large-vi-qa")
    tokenizer = AutoTokenizer.from_pretrained("ancs21/xlm-roberta-large-vi-qa")
    # Create a question answering pipeline
    qa_pipeline = pipeline("question-answering", model=model, tokenizer=tokenizer)
    # Get the answer
    answer = qa_pipeline(question=question_, context=context_)
        return answer