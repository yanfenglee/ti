from ti import T, run

tests = [
    T(name='test simple', path='/get',method='get'),
    T(name='test post data', path='/post',method='post',data={"Token":'d2d3ww'}, expect={'$.headers.Content-Type': 'application/json','$.json.Token':'d2d3ww'},ctx={'login_token':'$.json.Token'}),

    T(name='test error', path='/post',method='post', expect={'$.json.data':'no data'}),

    [
        T(name='test token variable', path='/anything',method='get',headers={'token':'$.login_token'},expect={'$.headers.Token':'d2d3ww'}),
    ]*3
]

run(tests, host='https://httpbin.org', verbose=False)
