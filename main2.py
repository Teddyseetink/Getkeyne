from flask import Flask, request, jsonify
from datetime import datetime
import hashlib,time,os,math,requests, json,string,random
app = Flask(__name__)
# text = "gg"
# data = text.encode()
# h = hashlib.sha256(data).hexdigest()
# print(h)
def encode_md5(text: str) -> str:
    encoded_text = text.encode("utf-8")
    md5_hash = hashlib.md5(encoded_text)
    return md5_hash.hexdigest()

def random_string(length: int = 8) -> str:
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def isfile(p):
    return os.path.exists(p)
def writefile(p, w):
    with open(p, "w", encoding="utf-8") as f:
        f.write(w)
        f.close()

def readfile(p):
    return open(p, "r", encoding="utf-8").read()

def checkkey(key: str):
    if not isfile("pkhanh.txt"):
        writefile("pkhanh.txt", "{}")
    
    data = json.loads(readfile("pkhanh.txt"))
    if data.get(key):
        if time.time() - data.get(key) < 86400:
            return True
        else:
            return False
    else:
        return False
def getkey_(hwid) :
    if not isfile("pkhanh.txt"):
        writefile("pkhanh.txt", "{}")
    
    data = json.loads(readfile("pkhanh.txt"))
    if data.get(hwid):
        if time.time() - data.get(hwid).get("time") < 86400:
            # print("thua")
            return data.get(hwid).get("key")
        else:
            should_hash_md5 = random_string(15) + str(time.time())
            new_key = "Key_" + encode_md5(should_hash_md5)
            data[hwid] = {
                "time": time.time(),
                "key": new_key
            }
            writefile("pkhanh.txt", json.dumps(data))
            return new_key
    else:
        should_hash_md5 = random_string(15) + str(time.time())
        new_key = "Key_" + encode_md5(should_hash_md5)
        data[hwid] = {
            "time": time.time(),
            "key": new_key
        }
        writefile("pkhanh.txt", json.dumps(data))
        return new_key

def getshortenlink(url):
    if not isfile("alllinkshortensaved.txt"):
        writefile("alllinkshortensaved.txt", "{}")

    data = json.loads(readfile("alllinkshortensaved.txt"))
    if not data.get(url):
        response = requests.get("https://link4m.co/api-shorten/v2?api=67f50b1962c3c943e43d2d2d&url=" + url)
        # print(requests.get("https://link4m.co/api-shorten/v2?api=67f50b1962c3c943e43d2d2d&url=" + url).text)
        jsondata = response.json()
        if jsondata.get("shortenedUrl"):
            data[url] = jsondata.get("shortenedUrl")
            writefile("alllinkshortensaved.txt", json.dumps(data))
            return jsondata.get("shortenedUrl")
    
    return data.get(url)

def tick():
    utc_now = time.time()
    offset = (datetime.now() - datetime.utcnow()).total_seconds()
    return utc_now + offset

def join_script(ok):
    okok = {
        "1": "m__o_t",
        "2": "_hai_",
        "3": "three__",
        "4": "four_bon",
        "5": "five_ne",
        "6": "sau_36",
        "7": "that__",
        "8": "bat_tam__",
        "9": "chin_9",
        "0": "_khonggg_"
    }
    new = ""
    old = str(ok)
    for i in old:
        new += okok[i]
    return new
apikey = "noguchihyuga"


@app.route('/getkey', methods=["GET"])
def getkey():
    try:
        # hwid_ = request.args.get("hwid")
        hwid_ = None
        for i, v in request.headers.items():
            if "fingerprint" in str.lower(i):
                hwid_ = v
                break
        if not hwid_:
            return "Not found HWID! Try other executors."
        
        key_valid_real = getkey_(hwid_)
        print(key_valid_real)
        okok = getshortenlink(f"https://noguchihyuga.github.io/authentication/TeddyHub/key.html?key={key_valid_real}")
        new_url = "https://noguchihyuga.github.io/authentication/TeddyHub/get.html?redirect="+ okok.replace("https://link4m.com/", "") if okok else "NONE"
        return new_url
    except Exception as e:
        print(e)
        pass
    return "Whitelist Check Error! Try later."

@app.route('/check', methods=["POST", "GET"])
def check():
    try:
        time_ = math.floor(tick())
        time_formated = join_script(time_)
        # data__ = request.get_json()
        key_ = request.args.get("key")
        hwid_ = None
        for i, v in request.headers.items():
            if "fingerprint" in str.lower(i):
                hwid_ = v
                break

        if not key_:
            return "Not Found Key!"
        elif not hwid_:
            return "Not found HWID! Try other executors."
        else:
            key_real_valid = getkey_(hwid=hwid_)
            if key_real_valid == key_:
                should_hash = time_formated + key_ + apikey + apikey[::-1] + key_[::-1] + time_formated[::-1]
                # print(should_hash)
                hashed = hashlib.sha256(should_hash.encode()).hexdigest()
                print(hashed)
                print(hwid_)
                # print(time_)
                return hashed
            else:
                return "Invalid Key"
    except Exception as e:
        print(e)
        pass
    return "Whitelist Check Error! Try later."

app.run(debug=True,port=9411)
