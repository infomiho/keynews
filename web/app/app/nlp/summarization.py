from gensim import summarization


def summarize(article):
    try:
        return summarization.summarizer.summarize(article.content, word_count=200)
    except ValueError as e:
        print (article)
        return ''
    except Exception as e:
        raise e
