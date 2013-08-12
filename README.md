Old code...may be incomplete or missing data....reference at your own risk

StockSentimentNN
================
Introduction
----------------

  Over the past several years interest in sentiment analysis of social media streams has exploded and there has been heavy commercialization of text-mining and social media channel mining. In fact, the text-analytics industry has grown to be worth over 1-billion dollars . While the majority of these efforts have been focused on brand monitoring tools, there has also been a major effort to track the general sentiment across companies and Twitter as a whole with the goal of predicting future stock market moves.
	While using Twitter as a canary for future stock market moves may seem novel, it is actually just the latest sentiment indicator for predicting market behavior. For nearly a century investors have been attempting to quantify consumer confidence, business sentiment and various other metrics as a sort of bellwether for the general direction of the economy. Twitter simply provides another signal for investors.
	In this project I explore using neural networks to make a prediction of tomorrows market direction by using 4 sentiment indicators including a numerical indicator for sentiment across the SNP500 companies with Twitter accounts.

Previous Work
----------------

There has been a proven correlation (with some delay) of overall Twitter sentiment and the direction that a stock will take . These techniques, however, don’t take into account other sentiment indicators outside of Twitter and simply make a prediction based on the overall mood of the company’s geed itself. 
There has been a great deal of effort to utilize neural networks within the arena of finance.  They have been proven to be fantastic tools for arbitrage, trade signaling and a number of other arenas that aren’t widely publicized in order to keep a competitive advantage. In terms of sentiment indicators – while I could find no specific use of classical indicators such as consumer confidence surveys, I have no doubt that they’ve been experimented with internally in trading houses. However, I have not come across any literature that combines classical economic mood bellwethers with Twitter sentiment measures.



Tool Choices
----------------

After some initial experimentation with WEKA and Matlab, I decided to use a Python package called PyBrain. PyBrain has a number of classes to handle building, training and evaluation neural networks. Ultimately the decision to use PyBrain was driven by a combination of comfort (I found WEKA frustrating to import data into) to economic (I didn’t want to purchase the Neural Network package). Additionally, it offered me the opportunity to evaluate a python machine-learning package for future use in a full system.
PyBrain itself is not terrifically documented, although it’s quick start guide is sufficient for gaining some traction and quickly getting a network up and running. 

The Approach
----------------

The initial design of the neural network was a simple feed-forward network with two output classes – one for positive predicted move at the close of tomorrow’s market, and one for a negative move at the close of tomorrow’s market. Initial testing indicated this worked well, however, I quickly found that a recurrent neural network with a single hidden layer seemed to work with better results. Intuitively, this makes sense since trends in the stock market continue over time. Testing with Pybrain however masked two large errors in my approach that I discovered after investing a large amount of time.
Firstly, one of the datasets I was using was incorrect. Due to a transcription error, I had accidently populated invalid data and trained the neural network on it. It wasn’t until I was building the validation data set that this became apparent. Secondly, I realized that there was an error in the output representation. PyBrain will, unless explicitly told not to, set the output dimensions to the size of the target vector. The target vector in my case has a dimension of 1 (with two possible values). This actually didn’t become apparent until attempting to test 5 trained networks on the validation set. I ended up having to retrain all of my networks.
I ended up explicitly specifying the classes to [0,1].  After that, I restarted the cycle of adjusting and testing parameters within my development data set. Theses adjustments included changing the weight decay, momentum,  and the size of the hidden layer. Finally, when I was satisfied with the results on the dev sets, I ran it against the validation data set.
Lastly, the hidden layer’s activation function was a standard Sigmoid function:
 
This was chosen because the literature suggested it worked well with the Back Propagation algorithm .

#Data Sets
	
The input vector to the neural network consists of 5 distinct pieces of data at a time t. The time corresponds to open market trading days. The first four pieces of data are inputs, the last is a target or output.  I had roughly 8 months of data. I used the first 6 as a training set splitting, at random, 75% for training and 25% as a development set. The last 2 were used as my gold test set.

###Downside Hedge Twitter Sentiment Tracker


The “Downside Hedge” is a stock trader information site that provides data an index of “sentiment” across the SNP500. They primarily market these Twitter indicators as additional tools for technical analysis . This data is released daily.

###Consumer Confidence Index (Conference Board)

The Consumer Confidence Index is one of two leading consumer sentiment indicators widely used by economists. The other index is put out by the University of Michigan (although it’s released on a less frequent basis).  The data is released monthly.

###New Housing Starts

The housing market in the U.S. is one of the largest industries – home ownership is an enshrined component of the American Dream. Construction also supports a number of industries and employs millions of Americans. As a result, New Housing Starts are a good indicator for both consumer sentiment and the confidence that home builders have in the future of the economy.  This data is released monthly by the Federal Reserve Bank of St Louis .

###SNP 500 Daily Close

The daily closing value of the SNP500 was the final input source for our data. The data was sourced using the Yahoo Stock Data API.

###Target Data

The target vector was simple a [0,1] vector.  0 if the price goes down at close of the next market trading day, 1 if the price goes up at the close of the next market trading day.

Training and Results
----------------

An initial attempt to train until convergence failed after 8 hours.  While this may have been due to the configuration of the Neural Network itself, I wanted to test a number of different configurations, decay and momentum values and having a single network clog the pipeline for 8 hours at a time wasn’t feasible.  As a result I limited the training period to 100,000 epochs.  This brought down the training time to roughly 2.5 hours. Additionally, 5 networks were being trained and tested at any given time, although output was going to the standard console so there was still a level of user interaction in the process.
In the end the best results with a recurrent neural network were: 

Hidden Layer Size	Momentum	Weight Decay	Training Error Rate	Test Error Rate	Gold Error Rate
6 Nodes	0.23	0.1	~54%	~37%	40%

Discussion, Future Work and Conclusion:
-----------------

As a predictive tool, this ensemble of indicators does slightly better than random but still worse than the prediction on Twitter sentiment along against the Dow Jones Industrial Index .  Although it’s not an apples to apples comparison since the attempt here was to predict the next day and the previous research indicates that Twitter prediction is best a few days out. Either way, I would not use this alone to replace traditional investment analysis.
The most critical component to this process was the acquisition and “massaging” of the data to fill the matrix. The data sources themselves are released at various intervals, so there is quite a bit of code to fill in the blanks. While I knew some effort would be involved in finding and sorting/cleaning the data I severely underestimated the actual effort needed in this task.  
  
Another take-away has to do with the technology choice – while PyBrain is mostly fully featured, there is no easy way to test a single vector against a classification network. In fact, network testing can be done only on data sets and, even then, there is no way of pulling out data for a confusion matrix from a series of data without extending the framework.  While there is built in support for Square Means evaluation, this is not the best evaluation metric for classification tasks. 
Moving forward, an implementation of cross-validation would likely provide better results: the current method of training simply splits the test and training datasets into random section of 75% and 25% respectively. Additionally, I would like to do some analysis of what the best features are within the neural network. Unfortunately, I couldn’t discover a way of doing this with PyBrain.
Lastly, it may be worth exploring alternative methods for using these data sources. In particular, a cluster based classification technique may be worth exploring (over a number of time intervals in the future). Lastly, the Twitter Sentiment indicator itself is synthesized over the entire SNP500 Twitter streams; this may not be the best the approach considering that individual stocks are much more sensitive to their own local channel sentiment than the SNP500 in aggregate.  
