from faker import Faker
fake_data = Faker("ar-SA")
# for attr in list(dir(fake_data)):
#     print(attr)

print(fake_data.prefix_male())
print(fake_data.name_male())
print(fake_data.address())


print("")
fake_data = Faker("en-US")
print(fake_data.prefix_male())
print(fake_data.name_male())
print(fake_data.address())




