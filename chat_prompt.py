import openai
import json

from g2pk import G2p

g2p = G2p()

with open('./config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config['DEFAULT']['API_KEY']

completion = openai.ChatCompletion.create(
    model = 'gpt-3.5-turbo',
    messages = [
        {
            "role": "system",
            "content": "Role: 어린이용 동화를 작성하는 전문 동화 작가\
                        Task: 당신은 어린아이의 이름과 정보를 받아서 그에 맞는 동화를 작성해야 합니다.\
                                기본적인 동화의 틀은 제시되는 동화의 흐름을 벗어나지 말아주세요.\
                                당신은 다음과 같은 동화의 틀이 제시되면 예시처럼 동화를 작성해야 합니다.\
                                ```작은 마을에 사랑스러운 {age}살 {gender} {name}가 살고 있었어요.\
                                {name}는 사랑스러운 가족들, 그리고 친구들과 즐거운 시간을 보내며 행복하게 살아가고 있었어요.\
                                어느 날, {name}의 부모님이 {name}에게 {favorite}을 선물해주셨어요.\
                                '이건 {name}의 {age}살 생일선물이란다. 생일이 되면 {favorite}가 {name}를 아름다운 곳으로 데려가줄거야.'\
                                ```\
                                ```작은 마을에 사랑스러운 7살 소녀 은희가 살고 있었어요.\
                                    은희는 사랑스러운 가족들, 그리고 친구들과 즐거운 시간을 보내며 행복하게 살아가고 있었어요.\
                                    어느 날, 은희의 부모님이 은희에게 커다란 토끼인형을 선물해주셨어요.\
                                    \'이건 은희의 일곱 살 생일선물이란다. 일곱번째 생일날이 되면 토끼가 은희를 아름다운 곳으로 데려가줄거야.'\
                                ```\
                                이제 age, gender, name, favorite 등의 정보와 함께 동화의 틀을 제시하겠습니다.",
        },
        {
            "role": "user",
            "content": "이 이야기의 주인공을 7살 소녀 은희로 바꿔서 각색해 줘. 은희는 토끼인형과 애니메이션을 좋아해",
        },
    ],
)

sent = completion['choices'][0]['message']['content']

print(sent)
print(g2p(sent))