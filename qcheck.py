from queue import PriorityQueue



queue = PriorityQueue()



queue.put((1, 3, "kek"))
queue.put((10, 2, "lol"))
queue.put((4, 5, "cda"))
queue.put((1, 2, "asdf"))
queue.put((4, 2, "kek"))
queue.put((5, 2, "ka"))
queue.put((2, 2, "ks"))
queue.put((45, 2, "kv"))
queue.put((2, 2, "kd"))





while not queue.empty():
    print(queue.get())
    










"""queue.put((0, 5, "kzxcv"))
queue.put((1, 2, "asdf"))
queue.put((1, 2, "kek"))
queue.put((1, 2, "ka"))
queue.put((1, 2, "ks"))
queue.put((1, 2, "kv"))
queue.put((1, 2, "kd"))"""