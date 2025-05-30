def longest_vowel_subsequence(s):
    vowels = 'aeiou'
    dp = [0] * 5  # dp[i] = max length ending with vowel vowels[i]
    for ch in s:
        if ch == 'a':
            dp[0] += 1
            print(f" a- {dp}")
        elif ch == 'e' and dp[0] > 0:
            dp[1] = max(dp[1], dp[0]) + 1
            print(f" e- {dp}")
        elif ch == 'i' and dp[1] > 0:
            dp[2] = max(dp[2], dp[1]) + 1
            print(f" i- {dp}")
        elif ch == 'o' and dp[2] > 0:
            dp[3] = max(dp[3], dp[2]) + 1
            print(f" o- {dp}")
        elif ch == 'u' and dp[3] > 0:
            dp[4] = max(dp[4], dp[3]) + 1
            print(f" u- {dp}")
    return dp[4]

def lvs1(data=None):
    vowels = 'aeiou'
    result = dict.fromkeys(vowels, 0)
    print(result)


print((longest_vowel_subsequence("eiou")))
print( [0] * 5)

