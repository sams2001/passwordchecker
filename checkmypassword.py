import requests
import hashlib 
import sys

def request_api_data(query_char):
    url = 'https://api.pwnedpasswords.com/range/' + query_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')
    return res

def get_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0

def pwned_api_check(password):
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char = sha1_password[:5]
    tail = sha1_password[5:]
    response = request_api_data(first5_char)
    return get_leaks_count(response, tail)


def main(password):
    count = pwned_api_check(password)
    if count:
        print(f"It was found {count} times... Consider changing your password")
    else:
        print("It was not found, you're ok!")
    print("")


filename = input("Enter the name of the .txt file with the passwords you would like to check ")
try:
    with open(filename, mode = 'r') as f:
        for i, password_in_txt in enumerate(f):
            password_in_txt = password_in_txt.strip()
            print(f"Checking password {i+1}")
            main(password_in_txt)
            
except:
    print("File not found, make sure it is a .txt file and you are spelling it correctly")
    