class Animal:
    __hungry = "yes"
    __name = "no name"
    __owner = "no owner"

    def __init__(self):
        pass

    def set_owner(self,newOwner):
        self.__owner= newOwner
        return

    def get_owner(self):
        return self.__owner

    def set_name(self,newName):
        self.__name= newName
        return

    def get_name(self):
        return self.__name

    def noise(self):
        print('Boughhhhhh')
        return

    def __hiddenmethod(self):
        print("hard to find")


def main():
    dog = Animal()
    dog.set_owner('Rajesh')
    print dog.get_owner()
    dog.noise()


if  __name__ =='__main__':
    main()
