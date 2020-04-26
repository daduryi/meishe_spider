from meishe.meishe_spider import MsSpider
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('''
        python3 run.py 2810203
        
        python3 run.py user_ids.txt
        
        user_ids.txt
        2810203
        2810201
        2810202
        ''')

    _, arg1 = sys.argv

    if arg1.isdigit():
        MsSpider.fetch(int(arg1))
    else:
        user_ids = []
        with open(arg1, encoding='utf8') as f:
            lines = f.readlines()

        for line in lines:
            user_ids.append(int(line.strip()))

        print(f'fetch {user_ids}')

        for user_id in user_ids:
            MsSpider.fetch(user_id)
