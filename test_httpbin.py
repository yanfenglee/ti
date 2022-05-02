from ti import T, run


ctx = {}
ctx['host'] = 'https://httpbin.org'
ctx['username'] = 'testname132'
ctx['postdata'] = {'testdata':123}

tests = [
    T(name='test get', url='/get',method='get'),
    T(name='test post', url='/post',method='post',data={"data":{"token":'asdf'}}, expect={'$.headers.Content-Type': 'application/json'},ctx={'login_token':'$.data.token'}),

    [
        T(name='test xxx', url='/api/v1/entries',method='post',headers={'token':'$.login_token'},data='$.postdata', expect={'code':'0'}),
    ]*3
]

run(tests, ctx, verbose=True)