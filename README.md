# ti
ti is a simple python auto test framework

## features

* use *expect* to ensure the response as expect
* use *ctx* dict to store variables and response values
* use jsonpath to reference the variable from ctx or response
* can restore response value in *ctx* with another name
* only one single python file, can integrate into your project very convinient

## install dependencies

> pip3 install requests jsonpath

## examples

```python
from ti import T, run

tests = [

    [
        T(name='login', path='/user/login',method='post',data={'username':'admin','password':'123456'}),
        T(name='get user', path='/user/info',method='post',headers={'Authorization':'Bearer $.token'},data={'id':'333'}),
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
```

simple output:

![output](output.png)

verbose output:

![output2](output2.png)