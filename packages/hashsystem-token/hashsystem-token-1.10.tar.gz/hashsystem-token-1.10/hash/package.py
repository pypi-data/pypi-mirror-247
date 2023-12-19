from datetime import datetime
from typing import Dict, List
import datetime


class HashMachenism:
    def __init__(self, seeds: Dict[str, List[int]]) -> None:
        self.seeds = seeds
        self.hashalgorithm = "x*y*z+a*b*c+w*q*x"
        self.alphabets = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        self.simbols = [
            "~",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "+",
            "=",
            "{",
            "}",
            "[",
            "]",
            ":",
            ";",
            "'",
            '"',
            "|",
            "/",
            ".",
            ",",
            "`",
        ]
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def hasspass(self, password):
        from datetime import datetime

        hashelements = self.hashalgorithm.split("+")
        hashpass = []
        hashed = "$RMA-"
        for index, x in enumerate(hashelements):
            lastindex = index
            for i in x.split("*"):
                passwordindex = self.get_pass_indexes(password)
                if lastindex == index:
                    wordpass = 1
                    for f in self.seeds["seeds"]:
                        wordpass *= f
                    hashpass.append(
                        [sum([z * wordpass for z in y]) for y in passwordindex]
                    )
        for ds in hashpass:
            for f in ds:
                if f < 0:
                    f = abs(f)
                for des in str(f):
                    hashed += self.alphabets[int(des)]
                    hashed += self.simbols[int(des)]
                    hashed += str(self.numbers[int(des)])
        return hashed

    def get_pass_indexes(self, password):
        passwordlistarrengements = []
        for i in self.alphabets:
            if i in password:
                passwordlistarrengements.append(
                    self.alphabets.index(i) - password.index(i)
                )
        passwordsimbolsarrenge = []
        for x in self.simbols:
            if x in password:
                passwordlistarrengements.append(
                    self.simbols.index(x) - password.index(x)
                )
        passwordnumbers = []
        for g in self.numbers:
            if str(g) in password:
                passwordnumbers.append(self.numbers.index(g) - password.index(str(g)))
        return passwordlistarrengements, passwordsimbolsarrenge, passwordnumbers

    def verify_password(self, hash_password, password):
        if self.hasspass(password) == hash_password:
            return True
        else:
            return False


class TokenGenerator:
    def __init__(self, payload: dict, seeds: list) -> None:
        self.payload = payload
        self.seeds = seeds
        self.hashalgorithm = "x*y*z+a*b*c+w*q*x"
        self.alphabets = [
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
            "g",
            "h",
            "i",
            "j",
            "k",
            "l",
            "m",
            "n",
            "o",
            "p",
            "q",
            "r",
            "s",
            "t",
            "u",
            "v",
            "w",
            "x",
            "y",
            "z",
            "A",
            "B",
            "C",
            "D",
            "E",
            "F",
            "G",
            "H",
            "I",
            "J",
            "K",
            "L",
            "M",
            "N",
            "O",
            "P",
            "Q",
            "R",
            "S",
            "T",
            "U",
            "V",
            "W",
            "X",
            "Y",
            "Z",
        ]
        self.simbols = [
            "~",
            "@",
            "#",
            "$",
            "%",
            "^",
            "&",
            "*",
            "(",
            ")",
            "-",
            "_",
            "+",
            "=",
            "{",
            "}",
            "[",
            "]",
            ":",
            ";",
            "'",
            '"',
            "|",
            "/",
            ".",
            ",",
            "`",
        ]
        self.numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.assignment = [self.alphabets, self.simbols, self.numbers]
        self.sep = [self.simbols[0], self.simbols[5]]

    def format_payload(self):
        dict_you_want = {
            key: self.payload[key] for key in list(self.payload.keys())[:-1]
        }
        return list(",".join(list(dict_you_want.values())))

    def get_time_int(self):
        return list(str(int(self.payload["exp"].timestamp())))

    def get_seeds_parms(self):
        seeds = [str(x) for x in self.seeds if type(x) == int]
        seeds[1] = self.seeds[1]
        seeds.append(self.seeds[2])
        return list(str(eval("{}{}{}".format(*seeds))))

    def get_hash_indexs(self):
        payload_indexes = []
        for x in self.format_payload():
            if x in self.alphabets:
                payload_indexes.append(self.alphabets.index(x))
            elif x in self.simbols:
                payload_indexes.append(self.sep[0])
                payload_indexes.append(self.simbols.index(x))
            elif int(x) in self.numbers:
                payload_indexes.append(self.sep[1])
                payload_indexes.append(self.numbers.index(int(x)))
        payload_indexes.append("_")
        for xs in self.get_time_int():
            if int(xs) in self.numbers:
                payload_indexes.append(self.sep[1])
                payload_indexes.append(self.numbers.index(int(xs)))
        payload_indexes.append("_")
        for cd in self.get_seeds_parms():
            if int(cd) in self.numbers:
                payload_indexes.append(self.sep[1])
                payload_indexes.append(self.numbers.index(int(cd)))
        return payload_indexes

    def divide_chunks(self, l, n):
        for i in range(0, len(l), n):
            yield l[i : i + n]

    def single_token_generation(self):
        token = ""
        for i, xs in enumerate(self.get_hash_indexs()):
            lasttype = None
            if type(xs) == int:
                if len(self.alphabets) >= xs and lasttype is None or lasttype == "numb":
                    token += self.alphabets[xs]
                    lasttype = "alpha"
                elif len(self.simbols) >= xs and lasttype == "alpha":
                    token += self.simbols[xs]
                    lasttype = "simb"
                elif len(self.numbers) >= xs and lasttype == "simb":
                    token += str(self.numbers[xs])
                    lasttype == "numb"
                elif len(self.simbols) <= xs and lasttype == "alpha":
                    tw = list(str(xs))
                    for x in tw:
                        token += str(self.simbols[int(x)])
                    lasttype = "simb"
                elif len(self.numbers) <= xs and lasttype == "simb":
                    te = list(str(xs))
                    for xe in te:
                        token += str(self.numbers[int(xe)])
                    lasttype == "numb"
            else:
                token += xs
        return token

    def decode_generated_token(self, token):
        val = ""
        sep = (0, False)
        for i, x in enumerate(list(token)):
            if x not in self.sep and not sep[1]:
                val += x
            elif x in self.sep:
                if x == self.sep[0]:
                    cs = token[i + 1]
                    if cs in self.alphabets:
                        val += self.simbols[self.alphabets.index(cs)]
                    elif cs in self.simbols:
                        val += self.simbols[self.simbols.index(cs)]
                    elif cs in self.numbers:
                        val += self.simbols[self.numbers.index(cs)]
                elif x == self.sep[1]:
                    cs = token[i + 1]
                    if cs in self.alphabets:
                        val += str(self.numbers[self.alphabets.index(cs)])
                    elif cs in self.simbols:
                        val += str(self.numbers[self.simbols.index(cs)])
                    elif cs in self.numbers:
                        val += str(self.numbers[self.numbers.index(cs)])
                sep = (i, True)
            elif sep[0] + 1 == i and sep[1]:
                sep = (0, False)
        return val

    def get_formetted_token(self, token):
        decoded = self.decode_generated_token(token).split("_")[:-1]
        return decoded

    def check_if_token_expired(self, token):
        date = int(self.get_formetted_token(token)[-1])
        dateT = datetime.datetime.fromtimestamp(date / 1e3)
        if datetime.datetime.now() > dateT:
            raise ValueError("token is Expired {}".format(token))
        else:
            return True

    def generate_refresh_token(self, days=7):
        self.payload["exp"] = self.payload["exp"] + datetime.timedelta(days=days)
        refresh_token = self.single_token_generation()
        self.payload["exp"] = self.payload["exp"] - datetime.timedelta(days=days)
        return refresh_token

    def get_token_pairs(self):
        return dict(
            access_token=self.single_token_generation(),
            refresh_token=self.generate_refresh_token(),
        )

    def token_from_refresh_token(self, refresh_token, duration=90):
        self.payload["exp"] = self.payload["exp"] + datetime.timedelta(days=duration)
        return self.get_token_pairs()
