def generator_function(n):
    while(n):
        n-= 1
        yield n

if __name__ == '__main__':
    for value in generator_function(7):
        print(value)