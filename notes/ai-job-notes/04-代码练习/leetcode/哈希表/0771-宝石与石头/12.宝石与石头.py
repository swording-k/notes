class Solution:
    def numJewelsInStones(self, jewels: str, stones: str) -> int:
        sum=0
        for x in stones:
            if x in jewels:
                sum+=1

        return sum