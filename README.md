# About
This is a demo solution requested as an tech interview trial task.
The objective of that is to develop a tool that analyses a given text and suggests improvements based on the similarity to a list of "standardised" phrases.

# Setup process
For Windows:
1. Get the code
- Checkout this repo

2. Get the data
- Download GoogleNews-vectors-negative300.bin from Kaggle (https://www.kaggle.com/datasets/sugataghosh/google-word2vec/)
- Unpack the downloaded archive and put the file into `app_backend\logic\models` folder. So the relative path is `app_backend\logic\models\GoogleNews-vectors-negative300.bin`

3. Run the solution
- Install/Start Docker-Desktop
- Go to the solution folder (where this readme is located) in the command line
- Run `docker-compose up` (or `make start`/`make stop` if you have Makefile installed)
- Open http://localhost:5173/ in your browser

After you open the page please expect the first run to be quite slow as the model file is being transformed into a more suitable format.

# Technologies used
- Python
- gensim
- sklearn

# Rationale behind the design decisions
First of all this is the first time I hit this kind of problem. After googling I found that in general the words similarity is solved by transforming them into vectors using pre-trained models. As I understand this technology is that each word can have multiple characterstics (in case of GoogleNews-vectors it is 300 characterstics/dimensions) so each word/vector can be compared to another word/vector to check whether they are very different or semantically close.

The next step was to understand how to deal with phrases. It looks like the how we go from words to phrases is just to sum up the vectors of the words (in fact I would expect to have average, but it seems it does not matter as the results were the same). However I am not sure this is the right way as it seems to me that while summing up we are losing the information about order of the words. Unfortunately I could not find a better solution so far.

The next step was to scan the input text and find the phrases that can be replaced. As the first step I split the text into sentences and then work with each sentence separately. I take each possible phrase (up to 5 words in a row) from the sentence and check versus the given stadard phrases. This generates a lot of suggestions. At first I cut out those suggestions which are lower than 0.1. And then do some filtering to find out the best suggestions to provide.

Overall I am not very satisfied with the results that my solution provides.
1. It produces very close suggestions which a human needs to post-process.
2. Some of the suggestions make no sense. E.g. it suggests to replace 'at our disposal' with 'utilize resources' with relatively high score 0.408 although the original phrase does not have any action/verb in it.
3. The suggestions do not match the original phrase grammatically. I imagine we can somehow calculate that the original phrase is in past tense and apply the same grammatical rule to the suggestion. I think we can generate synonym phrase for each of the standard phrase (using the same model) in different grammatical forms and then scan thru the synonyms and chech if some of them give higher score than the original standard phrase. I guess I need to spend more time on this algorithm and try to improve it.
