
# def functionB(f):
#     def functionC():
#         print("##########################################")
#         f()
#         print("******************************************")
#     return functionC
#
# @functionB
# def functionA():
#     print("Good Morning!")
#     return

#functionA()

def token_required(*args,**kwargs):
    def inner(f):
        print(f"value of optional is {kwargs['optional']}")
        f()
    return inner

@token_required(optional=1)
def get_users():
    print("I will give you all users")

