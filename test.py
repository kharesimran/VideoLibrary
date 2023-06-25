import requests

base_url = 'http://127.0.0.1:5000'
post_payload = {'name': 'Learn Flask', 'views': 1000, 'likes': 500}
headers = {'Content-Type': 'application/json'}
new_id = 2

response = requests.post('{}/video/{}'.format(base_url, new_id), json=post_payload, headers=headers)
post_payload['id'] = new_id
print('CREATE: ', 'OK' if response.json() == post_payload and response.status_code == 201 else 'Failed',
      response.json(),
      response.status_code)

response = requests.get('{}/video/{}'.format(base_url, new_id))
print('GET: ', 'OK' if response.json() == post_payload and response.status_code == 200 else 'Failed', response.json(),
      response.status_code)

put_payload = {'name': 'Learn React', 'views': 1100, 'likes': 600}
response = requests.put('{}/video/{}'.format(base_url, new_id), json=put_payload, headers=headers)
put_payload['id'] = new_id
print('UPDATE: ', 'OK' if response.json() == put_payload and response.status_code == 200 else 'Failed', response.json(),
      response.status_code)

response = requests.delete('{}/video/{}'.format(base_url, new_id))
print('DELETE: ', 'OK' if response.text == '' and response.status_code == 204 else 'Failed', response.text,
      response.status_code)

response = requests.get('{}/video/{}'.format(base_url, new_id))
print('GET DELETED: ' 'OK' if response.json() == {
    'message': 'Could not find a video with that ID.'} and response.status_code == 404 else 'Failed', response.json(),
      response.status_code)
