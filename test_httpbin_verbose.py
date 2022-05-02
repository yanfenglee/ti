from ti import T, run


ctx = {}
ctx['host'] = 'https://httpbin.org'

tests = [
    T(name='test get', url='/get',method='get'),
    T(name='test post', url='/post',method='post',data={"Token":'d2d3ww'}, expect={'$.headers.Content-Type': 'application/json','$.json.Token':'d2d3ww'},ctx={'login_token':'$.json.Token'}),

    [
        T(name='test xxx', url='/anything',method='get',headers={'token':'$.login_token'},expect={'$.headers.Token':'d2d3ww'}),
    ]*3,

    T(name='test error', url='/post',method='post', expect={'$.json.data':'no data'}),

]

run(tests, ctx, verbose=True)