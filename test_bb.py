from ti import T, run

tests = [

    [
        T(name='login', path='/user/login',method='post',data={'username':'admin','password':'123456'}),
        T(name='get user', path='/user/info',method='get',headers={'Authorization':'Bearer $.token'},params={'id':'333'}),
    ],
    
    [
        T(name='get user', path='/user/recordevt',method='post',headers={'Authorization':'Bearer $.token'},data={
            'user_id': 123,
            'platform': 'mini',
            'event_name': 'test event',
            'enable': True,
            'event_date': '20240811'
        }),
    ]*3
]

run(tests, host='http://localhost:8888')