from fuzzywuzzy import fuzz

# # nekiString1 = "website of faculty of organizational"
# # nekiString2 = "assistant go to the website of faculty of"

# # nekiString3 = nekiString2.lower().split()
# # nekiString3.pop(0)
# # print(' '.join(nekiString3[2:]))
# # similarity = fuzz.ratio((' '.join(nekiString3[2:])), nekiString1)
# # # similarity_ratio = fuzz.ratio(nekiString1, nekiString2) #outputs integer between 0 and 100
# # # print(similarity_ratio)
# # print(similarity)

nekiString1 = "assistant"
nekiString2 = "assistance"

similarity = fuzz.ratio(nekiString2, nekiString1)
print(similarity)

nekiString3 = nekiString2.lower().split()
nekiString3.pop(0)
print(' '.join(nekiString3[2:]))

similarity = fuzz.ratio((' '.join(nekiString3[2:])), nekiString1)
print(similarity)

if ('e' in nekiString2) and ('student' in nekiString2):
    similarity = fuzz.ratio((' '.join(nekiString3[2:])), nekiString1)
    similarity *=1.2
# similarity_ratio = fuzz.ratio(nekiString1, nekiString2) #outputs integer between 0 and 100
# print(similarity_ratio)
print(similarity)



# from fuzzywuzzy import fuzz

# # string1 = "apple pie with vanilla ice cream"
# # string2 = "cherry pie with ice cream"
# string1 = "e student website"
# string2 = "the student website"

# similarity_ratio = fuzz.ratio(string1, string2)
# print(similarity_ratio)
# # Split the strings into words
# words1 = string1.split()
# words2 = string2.split()

# # Assign weights to individual words
# weights1 = [1.0 if word != "student" else 2.0 for word in words1]
# weights2 = [1.0 if word != "student" else 2.0 for word in words2]

# # Compute the weighted ratio
# similarity_ratio = fuzz.WRatio(" ".join(words1), " ".join(words2), weights1, weights2)
# print(similarity_ratio) # Output: 68
# print(type(weights1))

