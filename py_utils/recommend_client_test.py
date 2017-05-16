from recommend_client import getUserPreferenceModel

# preference = getUserPreferenceModel("xiaowang")
# assert preference is None
preference = getUserPreferenceModel("xiaoming")
print preference
print 'test pass'