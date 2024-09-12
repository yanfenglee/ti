from ti import T, run

tests = [

    [
        T(name='登录', path='/user/login',method='post',data={'username':'admin','password':'123456'}, restore={'token':'$.token'}),
        T(name='获取用户信息', path='/user/info',method='get',headers={'Authorization':'Bearer $.token'},params={'id':'333'}),
    ],
    
    [
        T(name='埋点测试', path='/user/recordevt',method='post',headers={'Authorization':'Bearer $.token'},data={
            'user_id': 123,
            'platform': 'mini',
            'event_name': 'test event',
            'enable': True,
            'event_date': '20240811'
        }),
    ]*30000
]

run(tests, host='http://localhost:8888', verbose=True)