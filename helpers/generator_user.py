from faker import Faker


fake = Faker()


def email_generator():
    generated_email = fake.email()
    return generated_email

def password_generator():
    generated_password = fake.random_number(8)
    return generated_password

def name_generator():
    generated_name = fake.first_name()
    return generated_name


