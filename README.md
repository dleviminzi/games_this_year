The goal of this project is to analyze community sentiment before and after the release of Cyberpunk 2077. The expectation is that there will be a visible increase in excitement leading up to its release date and then a steep drop. The sentiment model is implemented using the Hugging Face transformer library. Specifically, I used the BERTForSequenceClassification model. For training, I used a large (2,000,000) pool of steam reviews and their associated rating (thumbs up/down). This dataset was perfect because steam reviews and reddit posts tend to exhibit a similar range of lengths and expressions. 

Currently using the uncased-base set the accuracy reaches ~%80. Upon inspection of some of the reviews labeled incorrectly, I have realized that I should have set a floor on the length of the review. The model struggles when the reviews are only a few words. Additionally, there was of course a point at which I had to truncate reviews in order to feed them into the model. I often chose to take the first few hundred words in order to achieve this goal. However, typically reviews save their condensed opinion for the conclusion, so I should've taken the last few hundred words. The next round of training will reflect these changes.

note: The scraper is relatively easy to use. I plan on cleaning it and releasing it as a more general purpose tool for scrapping specified subreddits over a specified period of time.

note: the link below goes to a "write up" about this project.

https://share.streamlit.io/dleviminzi/cyberpunk_sentiment_analysis/main/st.py
