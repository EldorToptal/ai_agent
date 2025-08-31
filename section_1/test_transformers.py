from transformers import pipeline

summarizer = pipeline("summarization")
text = "Einstein’s starting insight was the equivalence principle: locally (in a small enough region of spacetime) the effects of a uniform gravitational field are indistinguishable from those of being in an accelerating reference frame. For instance, an astronaut in a sealed cabin cannot tell whether the “weight” she feels is due to Earth’s gravity or to the cabin’s constant upward acceleration."

summary = summarizer(text, max_length=30, min_length=5, do_sample=False)
print(summary[0])
