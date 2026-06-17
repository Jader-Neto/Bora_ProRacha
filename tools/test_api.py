import urllib.request, urllib.parse, json, sys

API_BASE = 'http://127.0.0.1:5000'

def get(path):
    req = urllib.request.Request(API_BASE + path)
    with urllib.request.urlopen(req) as r:
        return json.load(r)

def post(path, data):
    data_bytes = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(API_BASE + path, data=data_bytes, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req) as r:
        return json.load(r), r.getcode()

if __name__ == '__main__':
    try:
        print('GET /api/quadras')
        quadras = get('/api/quadras')
        print('quadras count =', len(quadras))

        print('\nPOST /api/signup')
        user_data = {'nome':'Teste','email':'teste+unico@example.com','telefone':'99999','senha':'senha123'}
        signup_resp, code = post('/api/signup', user_data)
        print('signup code, resp=', code, signup_resp)

        print('\nPOST /api/login')
        login_resp, code = post('/api/login', {'email':user_data['email'], 'senha':user_data['senha']})
        print('login code, resp=', code, login_resp)
        user_id = login_resp.get('id')

        print('\nPOST /api/reservations')
        reserva_body = {'user_id': user_id, 'local':'Quadra Teste','horario':'18:00 - 19:00','valor':'R$ 120,00','metodo':'Cartão','ultimos4':'4242'}
        res_resp, code = post('/api/reservations', reserva_body)
        print('create reservation code, resp=', code, res_resp)

        print('\nGET /api/users/{}/reservations'.format(user_id))
        user_res = get(f'/api/users/{user_id}/reservations')
        print('user reservations =', user_res)

        print('\nAll tests completed successfully')
    except Exception as e:
        print('ERROR:', e)
        sys.exit(1)
