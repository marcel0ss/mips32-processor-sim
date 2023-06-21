class Util:

    def count_min_bits(num):
        if num:
            it_num = num
            count = 0
            while it_num > 0:
                count += 1
                it_num >>= 1
            return count
        return 1

    def is_not_pwr_of_two(num):
        return num & (num - 1)

    def next_pwr_of_2(num):
        i = 1
        while i < num:
            i *= 2
        return i
