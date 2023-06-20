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
