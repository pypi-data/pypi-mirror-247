
class ValidatePalndrome:
    def __init__(self):
        self.strng = None
    
    def validate(self,strng):
        self.strng = strng
        l = 0
        h = len(self.strng) -1 

        while l<=h:
            if self.strng[l] != self.strng[h]:
                return False
            l += 1
            h -= 1
        return True

def main():
    test_str = "anna"
    print(ValidatePalndrome().validate(test_str))


if __name__ == "__main__":
    main()
    
    
    