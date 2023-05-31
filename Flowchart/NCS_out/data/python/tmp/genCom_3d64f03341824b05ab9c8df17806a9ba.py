public int minDistance(String word1, String word2) {
        int m = word1.length(), n = word2.length();
        
        int[] dp = new int[n + 1];
        for(int j = 0; j <= n; j++){
            dp[j] = j;
        }

        for(int i = 0; i < m; i++){
            int pre = dp[0];
            dp[0] = i + 1;
            for(int j = 0; j < n; j++){
                int tmp = dp[j + 1];
                if(word1.charAt(i) == word2.charAt(j)){
                    dp[j + 1] = pre;
                } else {
                    dp[j + 1] = Math.min(Math.min(dp[j], dp[j + 1]), pre) + 1;
                }
                pre = tmp;
            }
        }
        return dp[n];
    }