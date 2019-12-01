## Find Emoji and split it
## source site : 
## https://stackoverflow.com/questions/51217909/removing-all-emojis-from-text
## https://stackoverflow.com/questions/49921720/how-to-split-emoji-from-each-other-python


import re
import emoji
import functools
import operator


# 예를 들어 이런 애들이 있다고 해봐여 
# sample text
emoji_text = ["와 진짜 개웃기다 😂😂 미친거 아니냐" ,
              "가격 문의는 디엠으로 부탁드립니다🙏🙏" , 
              "꽃🌹보다 아름다운 당신 내 취향 저격!💘💘💘" , 
              "힘내자💪ㅠㅠ"]


emojilist = []

for text in emoji_text : 
    
    word = text
    #print(i)
    
    try :

        a = re.findall("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U0001F1F2-\U0001F1F4"  # Macau flag
                u"\U0001F1E6-\U0001F1FF"  # flags
                u"\U0001F600-\U0001F64F"
                u"\U00002702-\U000027B0"
        #        u"\U000024C2-\U0001F251" 이거 왜 한글 나오냐
                u"\U0001f926-\U0001f937"
                u"\U0001F1F2"
                u"\U0001F1F4"
                u"\U0001F620"
                u"\u200d"
                u"\u2640-\u2642"
                "]+", word, flags = re.UNICODE)

        a = list(set(a))


        for j in a : 
            em = j
            em_split_emoji = emoji.get_emoji_regexp().split(em)
            em_split_whitespace = [substr.split() for substr in em_split_emoji]
            em_split = functools.reduce(operator.concat, em_split_whitespace)

            emojilist += em_split
            
    except : 
        pass
		
		
emojilist # check the result

