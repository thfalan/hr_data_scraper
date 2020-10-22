import requests
from math import cos, pi, floor

def parse_challenge(page):
    """
    Parse a challenge given by mmi and mavat's web servers, forcing us to solve
    some math stuff and send the result as a header to actually get the page.
    This logic is pretty much copied from https://github.com/R3dy/jigsaw-rails/blob/master/lib/breakbot.rb
    """
    top = page.split('<script>')[1].split('\n')
    challenge = top[1].split(';')[0].split('=')[1]
    challenge_id = top[2].split(';')[0].split('=')[1]
    return {'challenge': challenge, 'challenge_id': challenge_id, 'challenge_result': get_challenge_answer(challenge)}


def get_challenge_answer(challenge):
    """
    Solve the math part of the challenge and get the result
    """
    arr = list(challenge)
    last_digit = int(arr[-1])
    arr.sort()
    min_digit = int(arr[0])
    subvar1 = (2 * int(arr[2])) + int(arr[1])
    subvar2 = str(2 * int(arr[2])) + arr[1]
    power = ((int(arr[0]) * 1) + 2) ** int(arr[1])
    x = (int(challenge) * 3 + subvar1)
    y = cos(pi * subvar1)
    answer = x * y
    answer -= power
    answer += (min_digit - last_digit)
    answer = str(int(floor(answer))) + subvar2
    return answer

def hkjc_post_request(url: str) -> str:
    headers = {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}
    with requests.Session() as s:
        r = s.get(url, headers = headers)
        if 'X-AA-Challenge' in r.text:
            challenge = parse_challenge(r.text)
            cookies = s.get(url, headers={
                'X-AA-Challenge': challenge['challenge'],
                'X-AA-Challenge-ID': challenge['challenge_id'],
                'X-AA-Challenge-Result': challenge['challenge_result']
            }).cookies  
        else:
            cookies = r.cookies

        r = s.post(url, cookies = cookies)

    return r.text

def hkjc_get_request(url: str) -> str:
    headers = {'User-agent': 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1'}
    with requests.Session() as s:
        r = s.get(url, headers = headers)
        if 'X-AA-Challenge' in r.text:
            challenge = parse_challenge(r.text)
            cookies = s.get(url, headers={
                'X-AA-Challenge': challenge['challenge'],
                'X-AA-Challenge-ID': challenge['challenge_id'],
                'X-AA-Challenge-Result': challenge['challenge_result']
            }).cookies  
        else:
            cookies = r.cookies

        r = s.get(url, cookies = cookies)

    return r.text