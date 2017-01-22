import requests

url = 'http://10.0.0.11/gpio/api/v1.0/'

while True:
    choice = input("pin [on|off] | get > ")
    choice = choice.lower()
    choicelist = choice.split()

    try:
        if choice == 'get':
            response = requests.get(url + 'pins/getstate')

        elif choice == 'quit':
            break

        elif choicelist[1] == 'on':
            response = requests.get(url + 'pins/{0}/1'.format(choicelist[0]))

        elif choicelist[1] == 'off':
            response = requests.get(url + 'pins/{0}/0'.format(choicelist[0]))



        print(response.text)
    except:
        print('something when wrong')

