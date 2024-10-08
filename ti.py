import requests
from jsonpath import jsonpath
import re
from datetime import datetime


# color text message
def white(s): return f"\033[00m {s}\033[00m"
def red(s): return f"\033[91m {s}\033[00m"
def green(s): return f"\033[92m {s}\033[00m"
def yellow(s): return f"\033[93m {s}\033[00m"
def purple(s): return f"\033[95m {s}\033[00m"
def cyan(s): return f"\033[96m {s}\033[00m"


# retrieve data from json path
def jp(data, path, default=None):
    v = jsonpath(data, path)
    if v and type(v) is list:
        return v[0]
    return default


# replace like $.aaa.bbb in str by ctx
def var_replace(src: str, ctx: dict):
    regex = r'(\$(?:\.\w+)*)'
    if re.fullmatch(regex, src):
        return jp(ctx, src)

    keys = re.findall(regex, src)
    for k in keys:
        val = jp(ctx,k,'')
        src = src.replace(k, str(val))

    return src


# recursive resolve jsonpath value with context
def resolve(val, ctx):
    if type(val) is str:
        return var_replace(val, ctx)
    elif type(val) in [int,float,bool]:
        return val
    elif type(val) is dict:
        new_dict = {}
        for k in val:
            new_dict[k] = resolve(val[k], ctx)
        return new_dict
    elif type(val) is list:
        new_list = []
        for v in val:
            new_list.append(resolve(v, ctx))
        return new_list
    else:
        return val


# if result as expect, expect use jsonpath: {"$.data.code": "0"}
def match_expect(result:dict, expect:dict):
    if expect is None:
        return True

    for k in expect:
        if expect[k] != jp(result, k):
            return False
    
    return True
    

# test single, add response to context
def apply_single(ts, ctx, verbose=False):
    resp = {}
    try:
        method = resolve(ts['method'], ctx)
        path = resolve(ts['path'], ctx)
        params = resolve(ts['params'], ctx)
        headers = resolve(ts['headers'], ctx)
        data = resolve(ts['data'], ctx)
        expect = resolve(ts['expect'], ctx)

        if verbose:
            print(f"{datetime.now()} begin request: method={method},path={path},params={params},headers={headers},data={data},expect={expect}")

        response = requests.request(method=method,url=ctx['host']+path,params=params,headers=headers,json=data)
        resp['raw'] = response.text

        res = response.json()

        if match_expect(res, expect):
            ctx |= res
            ctx |= resolve(ts['ctx'], ctx)
            return True, path, res if verbose else ""
        else:
            return False, path, f" {res} {white('~~~===')} {purple(expect)}"
    except Exception as ex:
        return False, path, f" exception: {ex.args}, response: {resp['raw']}"


# print test result
def print_result(t, idx, passed, path, info):
    if passed:
        print(f"{datetime.now()} {green('------ passed')}, {t['name']}, {'%5d' % idx},  {path}, {cyan(info)}")
    else:
        print(f"{datetime.now()} {red('!!!!!! failed')}, {t['name']}, {'%5d' % idx},  {path}, {yellow(info)}")


# construct test infomation
def T(path,name='',method='get',params={},headers={},data={},expect=None,restore={}):
    return {'path':path,'name':name,'method':method,'params':params,'headers':headers,'data':data, 'expect':expect,'ctx':restore}


# run all tests
def run(tests, host, verbose=False, ctx={}):
    ctx |= {'host':host}
    idx = 0
    for ts in tests:
        if type(ts) is list:
            for t in ts:
                print_result(t, idx, *apply_single(t, ctx, verbose))
                idx += 1
        else:
            print_result(ts, idx, *apply_single(ts, ctx, verbose))
            idx += 1
