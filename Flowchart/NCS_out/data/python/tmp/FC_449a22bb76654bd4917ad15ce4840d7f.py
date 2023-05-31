class Solution:  #fc:startStop CLASS [Solution]
    def twoSum(self, nums: List[int], target: int) -> List[int]:  #fc:startStop "FUNC [twoSum]: enable or disable layer ."
        n = len(nums)
        for i in range(n): #fc:forLoop "LOOP" 
            for j in range(i + 1, n): #fc:forLoop "LOOP" 
                if nums[i] + nums[j] == target:  #fc:ifBranch "IF" 
                    return [i, j]  #fc:end "LOOP END"   #fc:end "LOOP END"   #fc:end "IF END"
        
        return []  #fc:startStop CLASS [Solution] END  #fc:startStop FUNC [twoSum]: END
