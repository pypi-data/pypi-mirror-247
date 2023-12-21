import itertools
class Phone:

    def __init__(self):
        # 中国移动号码段
        self.chinamobile = ["134", "135", "136", "137", "138", "139", "147", "150", "151", "152", "157", "158", "159",
                            "172", "178", "182", "183", "184", "187", "188", "198"]
        # 中国连通号码段
        self.chinaunicom = ["130", "131", "132", "145", "155", "156", "166", "171", "175", "176", "185", "186"]
        # 中国电信号码段
        self.chinatelecom = ["133", "149", "153", "173", "177", "180", "181", "189", "191", "199", "193"]

    def generate_phone_numbers(self, chinamobile=False, chinaunicom=False, chinatelecom=False):
        # 存放0-9数字，号码的4-11位从这里取
        num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        suffixes = [''.join(_) for _ in list(itertools.product(num, repeat=8))]

        phone_numbers = []
        if chinamobile:
            for prefix in self.chinamobile:
                for suffix in suffixes:
                    phone_numbers.append(f"{prefix}{suffix}")
        if chinaunicom:
            for prefix in self.chinaunicom:
                for suffix in suffixes:
                    phone_numbers.append(f"{prefix}{suffix}")

        if chinatelecom:
            for prefix in self.chinatelecom:
                for suffix in suffixes:
                    phone_numbers.append(f"{prefix}{suffix}")

        return phone_numbers


if __name__ == '__main__':
    phone = Phone()
    phone_numbers = phone.generate_phone_numbers(chinaunicom=True)
    print(phone_numbers[:5])
