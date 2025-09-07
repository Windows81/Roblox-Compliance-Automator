from collections import deque
import functools
import requests
import json
import os

COOKIES = {'.ROBLOSECURITY': os.environ.get('ROBLOSECURITY', '')}


def answer_question(q_dict: dict) -> int:
    return 0


@functools.cache
def get_questions(q_iden: str) -> list[dict]:
    http_response = requests.get(
        'https://apis.roblox.com/experience-questionnaire/v1/questionnaires/%s' % q_iden,
    ).json()
    return [
        question
        for section in http_response['questionnaire']['sections']
        for question in section['questions']
    ]


@functools.cache
def answer_questions(q_iden: str) -> list[tuple[str, str]]:
    questions = get_questions(q_iden)

    responses = []
    child_questions = deque(questions)
    while len(child_questions) > 0:
        question = child_questions.popleft()
        option_index = answer_question(question)
        option = question['options'][option_index]
        responses.append((question['id'], option['id']))
        child_questions.extendleft(option['childQuestions'])
    return responses


@functools.cache
def get_csrf():
    return requests.put(
        'https://apis.roblox.com/experience-questionnaire/v1/responses/1818/submissions',
        cookies=COOKIES,
    ).headers.get('x-csrf-token', None)


def process(place_iden: int):
    q_response = requests.get(
        'https://apis.roblox.com/experience-questionnaire/v1/questionnaires/%d/latest' % place_iden,
        cookies=COOKIES,
    )
    q_iden: str = q_response.json()['questionnaireId']
    responses = answer_questions(q_iden)
    payload = {
        'questionnaireId': q_iden,
        'response': {
            'answers': [
                {'questionId': q, "value": r'"%s"' % r}
                for (q, r) in responses
            ]
        }
    }
    return requests.post(
        'https://apis.roblox.com/experience-questionnaire/v1/responses/%d/submissions' % place_iden,
        cookies=COOKIES,
        headers={'x-csrf-token': get_csrf()},
        json=payload,
    )


if __name__ == '__main__':
    text = input("Enter universe iden(s), separated by commas: ")
    idens = [
        int(t.strip())
        for t in text.split(',')
    ]
    for iden in idens:
        result = process(iden)
        print('%17d - %s' % (iden, result))
