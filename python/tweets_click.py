N, K = [int(num) for num in input('N K>').split(' ')]
opened_tweets, all_tweets = [], [f'CLICK {i + 1}' for i in range(N)]

for num in range(K):
    click = input('>').upper()
    if click in opened_tweets and click in all_tweets:
        opened_tweets.remove(click)
    elif click not in opened_tweets and click in all_tweets:
        opened_tweets.append(click)
    elif click == 'CLOSEALL':
        opened_tweets.clear()
    print(f'>{len(opened_tweets)}')
