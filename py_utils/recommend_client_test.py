from recommend_client import getUserPreferenceModel

# preference = getUserPreferenceModel("xiaowang")
# assert preference is None
preference = getUserPreferenceModel("a@b.com")
print preference