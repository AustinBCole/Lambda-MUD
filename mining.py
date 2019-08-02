import hashlib
import requests
import uuid
import sys
import os
import time
import random


headers = { 'Authorization': 'token 72835a1eadb9d32cc63af8173e157b0a1a4ff7df',
    'content-type': 'application/json'}

def proof_of_work(last_proof, difficulty):
    """
    Simple Proof of Work Algorithm
    - Find a number p' such that hash(pp') contains 6 leading
    zeroes, where p is the previous p'
    - p is the previous proof, and p' is the new proof
    """

    print("Searching for next proof")
    proof = random.randint(10000,10000000000000000000000000000000000000)
    while valid_proof(last_proof, proof, difficulty) is False:
        proof += 1

    print("Proof found: " + str(proof))
    return proof


def valid_proof(last_proof, proof, difficulty):
    """
    Validates the Proof:  Does hash(last_proof, proof) contain 6
    leading zeroes?
    """
    guess = f'{last_proof}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:difficulty] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = int(sys.argv[1])
    else:
        node = "https://lambda-treasure-hunt.herokuapp.com/api/bc"

    coins_mined = 0
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof/", headers=headers)
        data = r.json()
        time.sleep(data['cooldown'])
        new_proof = proof_of_work(data.get('proof'), data['difficulty'])

        post_data = {"proof": new_proof}

        r = requests.post(url=node + "/mine/", json=post_data, headers=headers)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
