from data import  Data

def testAnalyze():
    #Settings
    count_url = 3                   #Кол-во используемых ссылок
    query = "gold in russian"      #Запрос
    count_word_in_head_for_dive = 3 #Кол-во слов, необходимое, чтобы перейти по ссылке
    max_count_dive = 3              #Кол-во слов, необходимое, чтобы перейти по ссылке

    data=Data()

    list_urls = data.getURLs(query)
    maxWordsFrequency=[]
    data.initTranslator()
    for url in list_urls:
        #Получение_веб_стрнички
        html = data.getHTML(url)
        if(len(html)<20):
         continue

        #Парсинг_и_перевод
        data.initSoup(html)
        text = data.getTextSoup()
        translation = data.getTranslate(text)

        #Анализ
        data.initTextBlob(translation.text)
        sentiment = data.getSentiment()
        maxWordsFrequency = data.getMaxFrequencyWords(20)

        data.listS.append(sentiment.polarity)
        data.listP.append(sentiment.subjectivity)
        data.listI.append(sentiment.polarity*sentiment.subjectivity)
        data.getVizulizeHistogram(maxWordsFrequency,url)

        print("Веб-страница: ",url)
        print("Слова: ",maxWordsFrequency)
        print("Сентимент: ",sentiment,"\n")

    data.getVizualizeGraphics()

test()

