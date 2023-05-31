def twoSum(nums, target):  #fc:startStop "FUNC [twoSum]: enable or disable layer ."
        n = len(nums)
        for i in range(n): #fc:forLoop "LOOP" 
            for j in range(i + 1, n): #fc:forLoop "LOOP" 
                if nums[i] + nums[j] == target:  #fc:ifBranch "IF" 
                    return [i, j]  #fc:end "LOOP END"   #fc:end "LOOP END"   #fc:end "IF END"
        
        return []  #fc:startStop FUNC [twoSum]: END
    
nums = [2,7,11,15]
target = 9
twoSum(nums, target)