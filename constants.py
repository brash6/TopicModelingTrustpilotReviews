import os

DIR_BASE = os.path.abspath(os.path.dirname(__file__))
DATA = os.path.join(DIR_BASE, 'data')
VIZ = os.path.join(DIR_BASE, 'viz')

TRAIN_REVIEWS1 = os.path.join(DATA, 'train_reviews.json')
TRAIN_REVIEWS2 = os.path.join(DATA, 'scraped_train_reviews.csv')

prefix = 'https://uk.trustpilot.com/review/www.'
prefix2 = 'https://uk.trustpilot.com/review/'
prefix3 = "https://uk.trustpilot.com/review/www.buytickets."
prefixes = [prefix3, prefix, prefix2]

en_stop = ['londonnorthwesternrailway', "hasn't", 'few', 'after', 'during', 'be', "needn't", 'each', 'mightn',
                    'not', 'even', 'right', 'should', "you're", 'train', "haven't", 'some', "that'll", 'or', 'through',
                    'on', 'weren', 'use', 'preston', 'and', 'say', 'every', 'thanks', 'its', 'himself', 'haven', "don't",
                    'why', 'these', 'shouldn', 'an', 'own', 'then', 'go', 'my', 'them', 'does', 'good', 'thank', 'because',
                    'over', 'more', "should've", 'nor', "you'll", 'aren', 'always', 'would', 'against', 'did', 'doesn',
                    'those', 'brussels', 'are', 'but', 'service', 'better', 'nationalrail', 'at', 'really', 'this', 'mustn',
                    'into', 'myself', 'he', 'again', "wasn't", 'only', 'try', 'make', 'who', 'isn', 'to', 'there', 'see',
                    'think', 'still', 'your', 'him', 'his', 't', 'didn', 'many', 'worst', 'll', 'with', "couldn't", 'out',
                    'such', 'don', 'ain', 'do', 'won', 'seem', 'where', 'can', 'take', 'as', 'how', 'theirs', "won't",
                    'grandcentralrail', 'virgintrains', 'euston', 'could', 'whom', 'needn', 'virgin', 'southeasternrailway',
                    'ticket', 'within', 've', 'it', 'am', "didn't", 'above', 'she', 'herself', 'off', 'further',
                    'yourselves', 'yourself', 'for', 'down', 'yours', 'under', 'ours', 'while', 'quite', 'will', 'below',
                    'hulltrains', 'eurostar', 'done', 'about', 'crosscountrytrains', 'a', "aren't", 'just', 'also',
                    'great', 'wasn', 'her', 'having', 'all', '_', 'no', 'lack', 'gwr', 'our', "she's", 'rather', 'now',
                    'shan', 'paddington', 'which', 'tpexpress', "you've", 'up', 'paris', 'review', 'so', 'once', 'run',
                    'doing', "shan't", 'too', 'very', 'edinburgh', 'their', 'we', 'arrivatrainswales', 'd', 'themselves',
                    'both', 'company', 'were', "mustn't", 'hers', 'never', "mightn't", 'by', 'line', 'is', 'come', 'going',
                    'of', 'was', 'being', 're', 'have', 'netherlands', 'what', 'chilternrailways', 'birmingham', 'southern',
                    "shouldn't", 'virgintrainseastcoast', 'the', 'you', 'when', 'ma', 'southernrailway', 'edu', 'in',
                    'easily', 'hasn', 'been', "wouldn't", 'hadn', 'ourselves', 'southwesternrailway', 'sleeper', 'easy',
                    'subject', "doesn't", 'want', "weren't", 'until', 'me', 'wouldn', 'itself', 'london', 'o', 'manchester',
                    'if', 'liverpool', 'know', 'than', 'm', "it's", 'any', 'most', 'getting', 'that', 'before', 'between',
                    'y', 'brussel', 's', 'may', 'lot', "isn't", 'eastmidlandstrains', 'need', 'often', 'nice', 'has',
                    'same', 'i', 'had', 'get', 'other', "you'd", 'northern', "hadn't", 'from', 'here', 'they', 'using',
                    'couldn', 'needed', 'customer', 'crewe', 'gatwick', 'railway', 'another', 'travel', 'travelling',
                    'travelled', 'chiltern', 'swindon', 'people', 'bristol', 'glasgow', 'national', 'french', 'amsterdam',
                    'mihaela', 'country', 'thing', 'belgium']
