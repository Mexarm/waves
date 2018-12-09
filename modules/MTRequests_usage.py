import MTRequests
from Queue import Queue
import requests

q = Queue()
def myprocess(value):
    id_, url = value
    try:
        r = requests.get(url)
        r.raise_for_status()
    except Exception as err:
        return dict(id = id_, error = err.message)
    return dict(id = id_, output = r.text)


for i in range(100):
    q.put((i,'https://httpbin.org/status/200'))
    q.put((i,'https://httpbin.org/user-agent'))
q.put((100,'https://httpbin.org/status/400'))
myworkers = MTRequests.MTRequests(q, myprocess,num_workers=50)
out = myworkers.run()
print list(out.queue)


