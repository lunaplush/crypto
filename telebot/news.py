class News:
    def __init__(self) -> None:
        pass


    def getNewsSentiment(newsData):
        negative, neutral, positive = float(newsData['negative']), float(newsData['neutral']), float(newsData['positive'])
        #print(type(negative))
        print(f"Negative: {negative} / Neutral: {neutral} / Positive: {positive}")
        if neutral > 0.5:
            return 'Neutral'
        if negative > positive:
            return 'Negative'
        else:
            return 'Positive'