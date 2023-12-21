import pywifi



class WiFi:

    def __init__(self):
        self.passwords = set()

    def _gen_password(self):
        character = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        number = "1234568790"

        pass

    def generate_china_phone_numbers(self):
        phone_numbers = []
        for i in range(130, 140):
            for j in range(10):
                for k in range(10):
                    phone_numbers.append("1{}{}{}".format(i, j, k))
        for i in range(150, 160):
            for j in range(10):
                for k in range(10):
                    phone_numbers.append("1{}{}{}".format(i, j, k))
        for i in range(170, 180):
            for j in range(10):
                for k in range(10):
                    phone_numbers.append("1{}{}{}".format(i, j, k))
        for i in range(180, 190):
            for j in range(10):
                for k in range(10):
                    phone_numbers.append("1{}{}{}".format(i, j, k))
        return phone_numbers