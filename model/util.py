from copyheaders import headers_raw_to_dict


def save_file(filename, text):
    with open(filename, 'w') as f:
        f.write(text)


def save_bfile(filename, text):
    with open(filename, 'bw') as f:
        f.write(text)


ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"

ua = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/7.0.12(0x17000c2c) NetType/WIFI Language/zh_CN"


def parse_raw_header(raw_header):
    return headers_raw_to_dict(bytes(raw_header, 'ascii'))
